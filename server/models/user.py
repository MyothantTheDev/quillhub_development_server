from mongoengine.fields import *
from mongoengine import Document, signals
import bcrypt

class User(Document):
  username = StringField(max_length=35, required=True)
  password = StringField(required=True, min_length=8)
  email = EmailField(required=True, unique=True)

  meta = { 'collection': 'users'}

  @classmethod
  def pre_save(cls, sender, document, **kwargs):
    # check if the password is already hashed.
    if not document.password.startwith("$2"):
      salt = bcrypt.gensalt()
      hashed = bcrypt.hashpw(document.password.encode('utf-8'), salt)
      document.password = hashed.decode('utf-8')

signals.pre_save.connect(User.pre_save, sender=User)