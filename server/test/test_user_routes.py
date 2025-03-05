import pytest
from server import Server
from server.models.user import User

user_json = {
  "username" : "Milly",
  "password" : "M!llyB0bby",
  "confirm_password" : "M!llyB0bby",
  "email" : "milly@gmail.com"
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
    'message': 'Login Successful.'
  }
  print(response.get_json())
  assert response.status_code == 200
  assert response.get_json() == res_message
  return response.get_json()

def test_user_deactivate(client, login_user):
  response = client.post("/account/deactivate")
  res_massage = {'status': 200, 'message': 'User account delected.'}
  assert response.status_code ==  200
  assert response.get_json() == res_massage