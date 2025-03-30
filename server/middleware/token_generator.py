from flask import current_app, request, jsonify
from flask_login import current_user
from server.models.user import User
from functools import wraps
import jwt
import datetime

# json web token generator
def token_generator(user : User):
  key = current_app.config['SECRET_KEY']
  expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
  user = {'user': user.to_dict(), 'expire': expire.date().isoformat()}
  return jwt.encode(user, key, algorithm="HS256")

def jwt_required(func):
  @wraps(func)
  def jwt_check(*args, **kwargs):
    try:
      encoded_cookies = [header.strip().split('=') for header in request.headers['Cookie'].split(';')]
      decoded_codkies = {}
      for key, value in encoded_cookies:
        decoded_codkies[key] =  value
      token = jwt.decode(decoded_codkies.get('token'), current_app.config['SECRET_KEY'], algorithms="HS256")
      if token['user']['id'] ==  str(current_user.id):
        return func(*args, **kwargs)
      return jsonify({'status': 401, 'message': {'error': 'Unauthorize token'}}), 401
    except:
      return jsonify({'status': 401, 'message': {'error': 'Unauthorize expire or lack token'}}), 401

  return jwt_check

def adminauthorized_required(func):
  @wraps(func)
  def authorization_check(*arg, **kwargs):
    try:
      user = User.objects(id__exact=current_user.id).first()
      if user.role.role == 'ADMIN':
        return func(*arg, **kwargs)
      return jsonify({'status': 401, 'message': {'error': 'Unauthorize role'}}), 401
    except:
      return jsonify({'status': 401, 'message': {'error': 'Unauthorize user'}}), 401
    
  return authorization_check