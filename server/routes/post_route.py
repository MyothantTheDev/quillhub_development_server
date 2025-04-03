from flask import Blueprint
from server.services import post_service
from server.routes.route_endpoints import (
  post_category, post_detial,
  post_comment, post_all
)

post_bp = Blueprint('posts', __name__)


# post routes
post_bp.add_url_rule(post_category, methods=['GET'], view_func=post_service.categories_articles)
post_bp.add_url_rule(post_detial, methods=['GET'], view_func=post_service.detail_article)
post_bp.add_url_rule(post_all, methods=['GET'], view_func=post_service.all_article)

# comment routes
post_bp.add_url_rule(post_comment, methods=['POST'], view_func=post_service.add_comment)