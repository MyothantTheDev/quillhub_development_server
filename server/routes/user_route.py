from flask import Blueprint
from server.services import user_services as users

users_bp = Blueprint('users', __name__)


users_bp.add_url_rule('/account', methods=['GET'], view_func=users.user_detail_service)
users_bp.add_url_rule('/account/update', methods=['POST'], view_func=users.user_update_service)
users_bp.add_url_rule('/register', methods=['GET'], view_func=users.account_register)