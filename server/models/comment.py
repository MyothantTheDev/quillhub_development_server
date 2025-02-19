from mongoengine.fields import *
from mongoengine import CASCADE
from mongoengine import Document
from server.models.article import Article
from server.models.user import User

class Comment(Document):
  article = ReferenceField(Article, reverse_delete_rule=CASCADE, require=True)
  user = ReferenceField(User, reverse_delete_rule=CASCADE, require=True)
  comment = StringField()

  meta = { 'collection' : 'comments'}