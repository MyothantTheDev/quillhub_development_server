from flask import Blueprint
from server.services import user_services as users

users_bp = Blueprint('users', __name__)

route_prefix = '/account/'

# user route constants
account_register = route_prefix+'register'
account_detail = route_prefix+'user'
account_login = route_prefix+'login'
account_logout = route_prefix+'logout'
account_delete = route_prefix+'deactivate'
account_update = route_prefix+'update'

# user routes
users_bp.add_url_rule(account_detail, methods=['GET'], view_func=users.user_detail_service)
users_bp.add_url_rule(account_update, methods=['POST'], view_func=users.user_update_service)
users_bp.add_url_rule(account_register, methods=['POST'], view_func=users.account_register)
users_bp.add_url_rule(account_login, methods=['POST'], view_func=users.user_login)
users_bp.add_url_rule(account_logout, methods=['GET'], view_func=users.user_logout)
users_bp.add_url_rule(account_delete, methods=['POST'], view_func=users.user_deactivate)