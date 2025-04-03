from mongoengine.fields import *
from mongoengine import EmbeddedDocument, Document
from flask import current_app
import os

# Define tuple for article block types
ArticleBlockType = (
  ('TITLE', 'title'),
  ('SUBTITLE', 'subtitle'),
  ('IMAGE', 'image'),
  ('PARAGRAPH', 'paragraph'),
  ('AUTHOR', 'author'),
  ('PUBLISH_DATE', 'publish_date')
)

TagType = (
  ('SCI', 'science'),
  ('MED', 'medical'),
  ('HIST', 'history'),
  ('TECH', 'technology'),
  ('MYTH', 'mythology'),
  ('MYST', 'mystery')
)

#An embedded document for a block within an article.
class ArticleBlock(EmbeddedDocument):
  type = StringField(choices=ArticleBlockType, required=True)
  text = StringField()
  image = StringField()
  serial_number = IntField(required=True)

  meta = { 'collection': 'articleblocks'}

  def to_dict(self):
    return {
      "type": self.type,
      "text": self.text,
      "image": os.path.join(current_app.root_path, 'media', self.image),
      "serial_number": self.serial_number
    }

#An embedded document for a teaser within an article.
class Teaser(EmbeddedDocument):
  title = StringField(required=True)
  image = StringField(required=True)
  text = StringField(required=True)

  def to_dict(self):
    return {
      'title': self.title,
      'image': self.image,
      'text': self.text
    }

#The main Article document.
class Article(Document):
  content = ListField(EmbeddedDocumentField(ArticleBlock))
  tags = ListField(StringField(choices=TagType))
  likes = IntField()
  teaser = EmbeddedDocumentField(Teaser)

  meta = { 'collection': 'articles' }

  def to_dict(self):
    return {
      "content": self.content.to_dict(),
      "tags": self.tags,
      "likes": self.likes,
      "teaser": self.teaser.to_dict()
    }