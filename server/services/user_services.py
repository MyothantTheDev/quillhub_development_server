from server.models.user import User
from server.models.favourite import UserFavouriteArticle
from server.schema.user_schema import RegisterSchema, ValidationError, LoginSchema
from flask import request, jsonify, session, make_response
from copy import deepcopy
from server.utils.token_generator import token_generator, jwt_required
from flask_login import login_user, current_user, logout_user, login_required
import bcrypt

# user profile
@jwt_required
@login_required
def user_detail_service():
  favourite_articles = UserFavouriteArticle.objects(user=current_user.id).select_related()
  articles = [fav.article for fav in favourite_articles]
  user_data = current_user.to_dict()
  user_data['favourite_articles'] = articles
  return {'status': 200, 'message': 'user detail', 'data': user_data}

# user update profile
@jwt_required
@login_required
def user_update_service():...

# user regiester
def account_register():
  request_cp : dict = deepcopy(request.json)
  try:
    validated_result = RegisterSchema().load(request_cp)
    user_check = User.objects(email__exact=validated_result.get('email')).first()
    if user_check:
      return jsonify(
        {
          'status': 200,
          'message': 'Email is already in used.'}
        )
    user = User(**validated_result)
    user.save()
    return jsonify(
        {
          'status': 200, 
          'message': f'Your account ({user.username}) has been created! You are now able to log in.',
       }
      )
  except ValidationError as err:
    return jsonify(
      {'status': 400, 'message': err.messages}
    )
  


# user login
def user_login():
  request_cp : dict = deepcopy(request.json)
  try:
    if current_user.is_authenticated:
      return {'status': 200, 'message': 'Already Login.'}
    validated_result = LoginSchema().load(request_cp)
    user = User.objects(email__exact=validated_result.get('email')).first()
    if user and bcrypt.checkpw(validated_result.get('password').encode('utf-8'), user.password.encode('utf-8')):
      login_user(user, remember=validated_result.get('remember'))
      jwtToken = token_generator(user)
      session['jwtToken'] = jwtToken
      response = make_response({'status': 200, 'message': 'Login Successful.'})
      response.set_cookie('token', jwtToken, httponly=True)
      return response
    return {'status': 401, 'message': 'Email or password is wrong or both!'}
  except ValidationError as err:
    return jsonify(
      {'status': 400, 'message': err.messages}
    )
  
@jwt_required
@login_required
def user_logout():
  logout_user()
  session.clear()
  response = make_response({'status': 200, 'message': 'User Logout.'})
  response.set_cookie('token', '', expires=0)
  response.set_cookie('remember_token', '', expires=0)
  return response

@jwt_required
@login_required
def user_deactivate():
  user = User.objects(id=current_user.id).first()
  if user:
    user.delete()
    logout_user()
    session.clear()
    response = make_response({'status': 200, 'message': 'User account delected.'})
    response.set_cookie('token', '', expires=0)
    response.set_cookie('remember_token', '', expires=0)
    return response
  return {'status': 400, 'message': 'Something went wrong.'}