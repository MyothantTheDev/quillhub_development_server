from flask import current_app, jsonify
from server.models.user import User
import jwt
import datetime

# json web token generator
def token_generator(user : User):
  key = current_app.config['SECRET_KEY']
  expire = datetime.datetime.utcnow() + datetime.timedelta(days=7)
  user = {'user': user.to_dict(), 'expire': expire.date().isoformat()}
  return jwt.encode(user, key, algorithm="HS256")