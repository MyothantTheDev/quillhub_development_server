import secrets
import os
from PIL import Image
from flask import current_app

def path_filename_generator(filename):
  MEDIA_FOLDER = os.path.join(current_app.root_path, 'media')
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(filename)
  filename = random_hex + f_ext
  return os.path.join(MEDIA_FOLDER, filename), filename

def save_picture(file):
  picture_path, picture_fn = path_filename_generator(file.filename)
  output_sz = (125, 125)
  i = Image.open(file)
  i.thumbnail(output_sz)
  i.save(picture_path)
  return picture_fn

def save_media(file):
  file_path, filename = path_filename_generator(file.filename)
  with open(file_path, 'wb') as f:
    f.write(file.read())
  return filename