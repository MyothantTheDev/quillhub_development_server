from flask import jsonify, request
from server.models.article import Article
from server.models.comment import Comment
from flask_login import current_user, login_required
from server.middleware.token_generator import jwt_required, adminauthorized_required
import re
import copy as cp

def all_article(page_number):
  try:
    re_pattern = r'\b\d+\b'
    if not re.fullmatch(re_pattern, page_number):
      return jsonify({'status': 401, 'message': 'Page number should be integer.'}), 401
    page_number = int(page_number)
    page_size = 5
    begin = (page_number - 1) * page_size
    end = begin + page_size
    articles = Article.objects[begin:end]()
    articles = [article.to_json() for article in articles]
    return jsonify(
      {
        'status': 200, 
        'message': 'Retrieved articles successful.',
        'data': articles
      }
      ), 200
  except:
    return jsonify(
      {
        'status': 401,
        'message': 'Something went wrong.'
      }
    ), 401
  

def categories_articles(category, page_number):
  try:
    re_pattern = r'\b\d+\b'
    if not re.fullmatch(re_pattern, page_number):
      return jsonify({'status': 401, 'message': 'Page number should be integer.'}), 401
    page_number = int(page_number)
    page_size = 5
    begin = (page_number - 1) * page_size
    end = begin + page_size
    articles = Article.objects(tags__in=[category])[begin:end]
    articles = [article.to_json() for article in articles]
    return jsonify(
      {
        'status': 200,
        'message': f'Retrieved {category} articles successful.',
        'data': articles
      }
    ), 200
  except:
    return jsonify(
      {
        'status': 401,
        'message': 'Something went wrong.'
      }
    )


def detail_article(post_id):
  comments = Comment.objects(article__exact=post_id).order_by('-comment_date')
  comments = [comment.to_json() for comment in comments]
  return jsonify({'status': 200, 'data': comments, 'message': 'Article related comments loaded.'}), 200

@jwt_required
@login_required
def add_comment():
  request_cp :dict = cp.deepcopy(request.json)

  try:
    if request_cp['post_id'] == None and request_cp['comment'] == None:
      return jsonify({'status': 401, 'message': 'Lacked of post id or message.'}), 401
    
    article = Article.objects(id__exact=request_cp['post_id']).first()
    if article == None:
      return jsonify({'status': 404, 'message': 'Article have been removed.'}), 404
    
    
    comment = Comment(article=article.id, user=current_user.id, comment=request_cp['comment'])
    comment.validate()
    comment.save()

    return jsonify({'status': 200, 'message': 'Comment added success.', 'data': comment.to_json()}), 200
  
  except:
    return jsonify({'status': 500, 'message': 'Something went wrong.'})