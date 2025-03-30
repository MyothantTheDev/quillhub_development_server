from flask import Blueprint
from server.services import post_service
from server.routes.route_endpoints import (
  post_trending, post_detial, post_delete,
  post_comment
)

post_bp = Blueprint('posts', __name__)


# post routes
post_bp.add_url_rule(post_trending, methods=['GET'], view_func=post_service.trending_articles)
post_bp.add_url_rule(post_detial, methods=['GET'], view_func=post_service.detail_article)
post_bp.add_url_rule(post_delete, methods=['POST'], view_func=post_service.delete_article)

# comment routes
post_bp.add_url_rule(post_comment, methods=['POST'], view_func=post_service.add_comment)