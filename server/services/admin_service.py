import json
from server.models.user import User
from server.models.article import Article, ArticleBlock, Teaser
from server.schema.user_schema import RegisterSchema, ValidationError
from flask import request, jsonify
from server.middleware.token_generator import adminauthorized_required, jwt_required
from server.utils.image_utils import save_media
from flask_login import login_required
import copy as cp

def register():
  resquest_cp : dict = request.json
  if resquest_cp['role'] == None:
    return jsonify({'status': 400, 'message': "Invaild request!"}), 400
  try:

    validated_result = RegisterSchema().load(resquest_cp, partial=True)

    user_check = User.objects(email__exact=validated_result.get('email')).first()
    if user_check:
      return jsonify({'status': 200, 'message': 'Email is already in used.'}), 200
    
    user = User(**validated_result)
    try:
      user.validate()
      user.save()
      return jsonify(
        {
          'status': 200,
          'message': f'Your account ({user.username}) has been created! You are now able to log in.'
        }
      ), 200
    except ValidationError as err:
      return {
        'status': 400,
        'message' : f'ValidationError: {err.messages}'
      }, 400
  
  except ValidationError as err:
    return jsonify(
      {'status': 400, 'message': err.messages}
    ), 400


@adminauthorized_required
@jwt_required
@login_required
def new_articles():
  try:
    content = request.form.get('content')
    files = request.files

    if not content:
      return jsonify({'status': 400, 'message': 'Content and files are required'}), 400
    
    try:
      content_blocks = json.loads(content)
    
    except json.JSONDecodeError:
      return jsonify({'status': 400, 'message': 'Invalid JSONFormat'}), 400
    
    article_blocks = []
    title = ''
    teaser_text = ''
    for block in content_blocks:
      if not all(k in block for k in ("type", "text", "serial_number")):
        return jsonify({'status': 400, 'message': 'Invalid content block format.'}), 400
      
      if block['serial_number'] == 0:
        title = block['text']
      if block['serial_number'] == 1:
        teaser_text = block['text']

      article_block = ArticleBlock(type=block['type'], text=block.get('text', ''), serial_number=block['serial_number'])
      article_block.validate()
      article_blocks.append(article_block)

    filename = ''

    if files:
      for serial_number, file in files.items():
        if file and file.filename:
          filename = save_media(file)
          article_block = ArticleBlock(type='IMAGE', image=filename, serial_number=serial_number)
          article_blocks.append(article_block)

    teaser = None
    if title != '' and teaser_text != '' and filename != '':
      teaser = Teaser(title=title, image=filename, text=teaser_text)
      teaser.validate()
          
    article = Article(
      content=article_blocks,
      likes=0,
    )
    if teaser != None:
      article.teaser = teaser
    article.save()

    return jsonify({'status': 200, 'message': 'Article created successfully'}), 200
  
  except Exception as err:
    return jsonify({'status': 500, 'message': str(err)}), 500
  
  
@adminauthorized_required
@jwt_required
@login_required
def delete_article():
  request_cp :dict = cp.deepcopy(request.json)

  if request_cp['post_id'] == None:
    return jsonify({'status': 400, 'message': 'Invalid post id.'}), 400
    
  try:
    article = Article.objects(id__exact=request_cp['post_id']).first()
    article.delete()
    return jsonify({'status': 200, 'message': 'Delete article successful.'}), 200
  except:
    return jsonify({'status': 500, 'message': 'Something went wrong.'}), 500