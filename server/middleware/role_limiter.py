from flask_login import current_user
from server.models.user import User
from flask import request

def get_user_role():
  requested_role = request.headers.get('X-User-Role', 'guest')
  if current_user:
    user_role = User.objects(id__exact=current_user.id).first().role.role
    return None if requested_role == "admin" and user_role == "admin" else requested_role
  return requested_role