from flask import Blueprint
from server.services import user_services as users

users_bp = Blueprint('users', __name__)


users_bp.add_url_rule('/account', methods=['GET'], view_func=users.user_detail_service)
users_bp.add_url_rule('/account/update', methods=['POST'], view_func=users.user_update_service)
users_bp.add_url_rule('/register', methods=['POST'], view_func=users.account_register)
users_bp.add_url_rule('/login', methods=['POST'], view_func=users.user_login)
users_bp.add_url_rule('/logout', methods=['GET'], view_func=users.user_logout)
users_bp.add_url_rule('/account/deactivate', methods=['POST'], view_func=users.user_deactivate)