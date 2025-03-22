from flask import Blueprint
from server.services import post_service

post_bp = Blueprint('posts', __name__)

# route prefix
route_prefix = '/post/'

# post route contansts
post_trending = route_prefix+'trending'
post_detial = route_prefix+'detial'
post_delete = post_detial+'/delete'
post_comment = route_prefix+'comment/add'

# post routes
post_bp.add_url_rule(post_trending, methods=['GET'], view_func=post_service.trending_articles)
post_bp.add_url_rule(post_detial, methods=['GET'], view_func=post_service.detail_article)
post_bp.add_url_rule(post_delete, methods=['POST'], view_func=post_service.delete_article)

# comment routes
post_bp.add_url_rule(post_comment, methods=['POST'], view_func=post_service.add_comment)