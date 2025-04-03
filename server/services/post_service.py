from flask import jsonify
from server.models.article import Article
from flask_login import current_user, login_required
from server.middleware.token_generator import jwt_required, adminauthorized_required
import re

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
    articles = Article.objects(tags=category)[begin, end]
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


def detail_article():...

@adminauthorized_required
@jwt_required
@login_required
def delete_article():...

@jwt_required
@login_required
def add_comment():...