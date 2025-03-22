import json
from server.models.user import User
from server.models.article import Article, ArticleBlock
from server.schema.user_schema import RegisterSchema, ValidationError
from flask import request, jsonify
from server.utils.token_generator import adminauthorized_required, jwt_required
from server.utils.image_utils import save_media
from flask_login import login_required, current_user

def register():
  resquest_cp : dict = request.json
  if resquest_cp['role'] == None:
    return {'status': 400, 'message': "Invaild request!"}
  try:
    validated_result = RegisterSchema().load(resquest_cp, partial=True)
    user_check = User.objects(email__exact=validated_result.get('email')).first()
    if user_check:
      return {'status': 200, 'message': 'Email is already in used.'}
    user = User(**validated_result)
    if user.validate():
      user.save()
      return jsonify(
        {
          'status': 200,
          'message': f'Your account ({user.username}) has been created! You are now able to log in.'
        }
      ), 200
    return {
      'status': 400,
      'message' : 'Something went wrong.'
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
    content = request.form.getlist('content')
    files = request.files.getlist('files')
    if not content:
      return jsonify({'status': 400, 'message': 'Content and files are required'}), 400
    content_blocks = json.loads(content)
    article_blocks = []
    for block in content_blocks:
      article_block = ArticleBlock(type=block['type'], text=block['content'], serial_number=block['serial'])
      article_blocks.append(article_block)
    if files:
      for file in files:
        filename = save_media(file['file'])
        article_block = ArticleBlock(type=file['type'], image=filename, serial_number=file['serial'])
        article_blocks.append(article_block)
    article = Article(
      title=request.form.get('title'),
      content=article_blocks,
      likes=0,
      author_id=current_user.id
    )
    article.save()
    return {'status': 200, 'message': 'Article created successfully'}, 200
  except Exception as err:
    return jsonify({'status': 500, 'message': str(err)}), 500