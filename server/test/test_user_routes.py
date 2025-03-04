import pytest
from server import Server
from server.models.user import User

user_json = {
  "username" : "Milly",
  "password" : "D@mnlove1500",
  "confirm_password" : "D@mnlove1500",
  "email" : "milly@gmail.com"
}

@pytest.fixture
def client():
  server = Server()
  app = server.set_up()
  app.config["TESTING"] = True
  server.connect()
  
  with app.test_client() as client:
    yield client

def test_register_pass(client):
  response = client.post("/register", json=user_json)
  user = User.objects(email__exact=user_json['email']).first()
  res_message = {
    "status": 200,
    "message": "Your account has been created! You are now able to log in.",
    "user": user.to_dict()
  }
  assert response.status_code == 200
  assert response.get_json() == res_message


  