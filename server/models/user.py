from mongoengine.fields import *
from mongoengine import Document, EmbeddedDocument,signals
import bcrypt
from flask_login import UserMixin

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

class User(Document, UserMixin):
  username = StringField(max_length=35, required=True)
  password = StringField(required=True, min_length=8)
  email = EmailField(required=True, unique=True)
  image = StringField()
  role = EmbeddedDocumentField(Role)

  meta = { 'collection': 'users'}

  @classmethod
  def pre_save(cls, sender, document, **kwargs):
    # check if the password is already hashed.
    if not document.password.startwith("$2"):
      salt = bcrypt.gensalt()
      hashed = bcrypt.hashpw(document.password.encode('utf-8'), salt)
      document.password = hashed.decode('utf-8')

  def to_dict(self):
    return {
      "id": str(self.id),
      "username": self.username,
      "email" : self.email
    }

signals.pre_save.connect(User.pre_save, sender=User)