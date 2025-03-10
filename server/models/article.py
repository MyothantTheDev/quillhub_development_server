from mongoengine.fields import *
from mongoengine import EmbeddedDocument, Document

# Define tuple for article block types
ArticleBlockType = (
  ('TITLE', 'title'),
  ('SUBTITLE', 'subtitle'),
  ('IMAGE', 'image'),
  ('PARAGRAPH', 'paragraph')
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

#The main Article document.
class Article(Document):
  content = ListField(EmbeddedDocumentField(ArticleBlock))
  tags = ListField(StringField(choices=TagType))
  likes = IntField()

  meta = { 'collection': 'articles' }