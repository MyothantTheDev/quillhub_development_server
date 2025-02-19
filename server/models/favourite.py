from mongoengine.fields import *
from mongoengine import Document
from mongoengine import CASCADE
from server.models.user import User
from server.models.article import Article

class UserFavouriteArticle(Document):
  user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
  article = ReferenceField(Article, reverse_delete_rule=CASCADE, required=True)

  meta = { 'collection': 'userfavouritearticles'}