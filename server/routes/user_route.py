from flask import Blueprint
from server.services import user_services as users
from server.routes.route_endpoints import (
  account_delete, account_detail, account_login, 
  account_logout, account_register, account_update 
)

users_bp = Blueprint('users', __name__)

users_bp.add_url_rule(account_detail, methods=['GET'], view_func=users.user_detail_service)
users_bp.add_url_rule(account_update, methods=['POST'], view_func=users.user_update_service)
users_bp.add_url_rule(account_register, methods=['POST'], view_func=users.account_register)
users_bp.add_url_rule(account_login, methods=['POST'], view_func=users.user_login)
users_bp.add_url_rule(account_logout, methods=['GET'], view_func=users.user_logout)
users_bp.add_url_rule(account_delete, methods=['POST'], view_func=users.user_deactivate)