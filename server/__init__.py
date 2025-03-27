from flask import Flask
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mongoengine2 import MongoEngine

load_dotenv(os.path.abspath(__name__)+'\\config\\quillhub.env')
_bcrypt = Bcrypt()
_login_manager = LoginManager()

class Server:

  _db = MongoEngine()
  
  def _mongo_config(self):
    return {
      "db": os.getenv('DB_NAME'),
      "host": os.getenv('DB_HOST'),
      "port": int(os.getenv('DB_PORT')),
      "username": os.getenv('DB_USER'),
      "password": os.getenv('DB_PWD'),
      "authsource": os.getenv('DB_NAME')
    }

  def _routes(self, app: Flask):

    from server.routes.user_route import users_bp # route module
    from server.routes.post_route import post_bp
    from server.routes.admin_routes import admin_bp

    app.register_blueprint(users_bp) # install user routes
    app.register_blueprint(post_bp) # install post routes
    app.register_blueprint(admin_bp) # install admin routes

  def set_up(self):

    mongo_settings = self._mongo_config()
    
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.getenv('SECRET_KEY'))
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config["MONGODB_SETTINGS"] = [
      mongo_settings
    ]

    _bcrypt.init_app(app) # encryption install
    _login_manager.init_app(app) # login manager install
    self._db.init_app(app)

    '''
    Routers
    '''
    self._routes(app)

    return app

  def start(self, debug=True, host='127.0.0.1', port=5000):
    app = self.set_up()
    app.run(debug=debug, host=host, port=port)