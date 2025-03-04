from mongoengine.fields import *
from mongoengine import Document, EmbeddedDocument,signals
import bcrypt
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer
from flask import current_app
from server import _login_manager

@_login_manager.user_loader
def load_user(user_id):
  return User.objects(id=user_id).first()

role_types = {
  ('ADMIN', 'admin'),
  ('MODIRATOR', 'modirator'),
  ('USER', 'user')
}

permission_types = (
  ('R', 'read'),
  ('W', 'write'),
  ('RW', 'readWrite'),
  ('RWD', 'readWriteDelete')
)

class Role(EmbeddedDocument):
  role = StringField(max_length=10, min_length=4, choices=role_types)
  permission = StringField(max_length=3, choices=permission_types)

  def to_dict(self):
    return {
      "role": self.role,
      "permission": self.permission
    }

class User(Document, UserMixin):
  username = StringField(max_length=35, required=True)
  password = StringField(required=True, min_length=8)
  email = EmailField(required=True, unique=True)
  image = StringField()
  role = EmbeddedDocumentField(Role)

  meta = { 'collection': 'users'}

  @classmethod
  def pre_save(cls, sender, document, **kwargs):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(document.password.encode('utf-8'), salt)
    document.password = hashed.decode('utf-8')

  def to_dict(self):
    return {
      "id": str(self.id),
      "username": self.username,
      "email" : self.email,
      "image": self.image,
      "role" : self.role.to_dict()
    }
  
  def get_reset_token(self, expire_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], )
    return s.dump({'user_id': self.id}).decode('utf-8')

signals.pre_save.connect(User.pre_save, sender=User)