import pytest
from server import Server
from server.models.user import User
from server.models.favourite import UserFavouriteArticle
from bson import ObjectId
from copy import deepcopy

user_json = {
  "username" : "Milly",
  "password" : "M!llyB0bby",
  "confirm_password" : "M!llyB0bby",
  "email" : "milly@gmail.com"
}

admin_user_json = {
  "username": "James",
  "password": "J@m3s12345",
  "confirm_password": "J@m3s12345",
  "email": "james@gmail.com",
  "role": "admin"
}

user_login = {
  'email': "milly@gmail.com",
  'password': 'M!llyB0bby'
}

@pytest.fixture
def client():
  server = Server()
  app = server.set_up()
  app.config["TESTING"] = True
  server.connect()
  
  with app.test_client() as client:
    yield client

def test_register(client):
  response = client.post("/register", json=user_json)
  res_message = {
    "status": 200,
    "message": f"Your account ({user_json['username']}) has been created! You are now able to log in.",
  }
  assert response.status_code == 200
  assert response.get_json() == res_message

@pytest.fixture
def login_user(client):
  response = client.post('/login', json=user_login)
  user = User.objects(email__exact=user_json['email']).first()
  res_message = {
    'status': 200,
    'message': 'Login Successful.',
    'data': user.to_dict()
  }
  assert response.status_code == 200
  assert response.get_json() == res_message
  return response.get_json()

def test_user_account(client, login_user):
  response = client.get('/account')
  user_id = ObjectId(login_user['data']['id'])
  data = deepcopy(login_user['data'])
  favourite_articles = UserFavouriteArticle.objects(user=user_id).select_related()
  articles = [fav.article for fav in favourite_articles]
  data['favourite_articles'] = articles
  res_message = {
    "status": 200,
    "message": "user detail",
    "data": data
  }
  assert response.status_code == 200
  assert response.get_json() == res_message

def test_user_logout(client, login_user):
  response = client.get('/logout')
  res_message = {
    'status': 200,
    'message': 'User Logout.'
  }
  assert response.status_code == 200
  assert response.get_json() == res_message


def test_admin_register(client):
  pass

def test_user_deactivate(client, login_user):
  response = client.post("/account/deactivate")
  res_massage = {'status': 200, 'message': 'User account delected.'}
  assert response.status_code ==  200
  assert response.get_json() == res_massage