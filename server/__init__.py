from flask import Flask
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from mongoengine import connect

load_dotenv('./config/quillhub.env')

class Server:
  
  def __init__(self):
    db_uri = os.getenv("DB_URI")
    connect(db_uri)
    self._bcrypt = Bcrypt()

  def _routes(self, app: Flask):
    app.register_blueprint()

  def start(self, debug=True, host='127.0.0.1', port=5000):

    app = Flask(__name__)
    app.config.from_mapping(SECREKT_KEY='2d7a8ec7b7e93a7c8e246e956b6ab73f')

    self._bcrypt.init_app(app)

    '''
    Routers
    '''
    self._routes(app)

    app.run(debug=debug, host=host, port=port)