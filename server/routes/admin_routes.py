from flask import Blueprint
from server.services import admin_service
from server.routes.route_endpoints import (
  admin_acc_register, admin_post_add
)

admin_bp = Blueprint('admin', __name__)



# account related route
admin_bp.add_url_rule(admin_acc_register, methods=['POST'], view_func=admin_service.register)

# post related route
admin_bp.add_url_rule(admin_post_add, methods=['POST'], view_func=admin_service.new_articles)