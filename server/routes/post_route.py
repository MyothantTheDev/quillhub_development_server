from flask import Blueprint
from server.services import post_service

post_bp = Blueprint('posts', __name__)

post_bp.add_url_rule('/post', methods=['GET'], view_func=post_service.trending_articles)
post_bp.add_url_rule('/post/add', methods=['POST'], view_func=post_service.new_articles)
post_bp.add_url_rule('/post/detail', methods=['GET'], view_func=post_service.detail_article)
post_bp.add_url_rule('/post/detail/delete', methods=['POST'], view_func=post_service.delete_article)