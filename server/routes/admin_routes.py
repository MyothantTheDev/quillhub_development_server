from flask import Blueprint
from server.services import admin_service

admin_bp = Blueprint('admin', __name__)

route_prefix = '/admin/'

# account related route
  # route constants
admin_acc_register = route_prefix+'register'

  # route rules
admin_bp.add_url_rule(admin_acc_register, methods=['POST'], view_func=admin_service.register)

# post related route
  # route constants
admin_post_add = route_prefix+'post/new'

  # route rules
admin_bp.add_url_rule(admin_post_add, methods=['POST'], view_func=admin_service.new_articles)