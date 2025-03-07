import secrets
import os
from PIL import Image
from flask import current_app

def save_picture(file):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(file.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(current_app.root_path, 'media', picture_fn)
  output_sz = (125, 125)
  i = Image.open(file)
  i.thumbnail(output_sz)
  i.save(picture_path)
  return picture_fn