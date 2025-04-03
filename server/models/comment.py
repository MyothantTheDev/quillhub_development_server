from mongoengine.fields import *
from mongoengine import CASCADE, DateTimeField
from mongoengine import Document
from server.models.article import Article
from server.models.user import User
from datetime import datetime as dt

class Comment(Document):
  article = ReferenceField(Article, reverse_delete_rule=CASCADE, require=True)
  user = ReferenceField(User, reverse_delete_rule=CASCADE, require=True)
  comment = StringField()
  comment_date = DateTimeField(default=dt.now, required=True)

  meta = { 'collection' : 'comments'}