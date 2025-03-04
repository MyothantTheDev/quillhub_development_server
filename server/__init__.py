from flask import Flask
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from mongoengine import connect
from flask_login import LoginManager

load_dotenv(os.path.abspath(__name__)+'\\config\\quillhub.env')

_bcrypt = Bcrypt()
_login_manager = LoginManager()

class Server:
  
  def connect(self):
    db_uri = os.getenv('DB_URI')
    connect(host=db_uri)
    

  def _routes(self, app: Flask):

    from server.routes.user_route import users_bp # route module

    app.register_blueprint(users_bp) # install user routes

  def set_up(self):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.getenv('SECRET_KEY'))
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    _bcrypt.init_app(app) # encryption install
    _login_manager.init_app(app) # login manager install

    '''
    Routers
    '''
    self._routes(app)

    return app

  def start(self, debug=True, host='127.0.0.1', port=5000):
    self.connect()
    app = self.set_up()
    app.run(debug=debug, host=host, port=port)