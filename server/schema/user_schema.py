from marshmallow import Schema, validate, validates, ValidationError, fields, post_load
import re

class RegisterSchema(Schema):
  id = fields.String(dump_only=True)
  username = fields.String(validate=validate.Length(min=2, max=20), required=True)
  password = fields.String(required=True, load_only=True)
  confirm_password = fields.String(required=True, load_only=True)
  email = fields.Email()

  @validates('password')
  def validate_password(self, value):
    if len(value) < 8:
      raise ValidationError('Password must have minmum 8 characters length.')
    if not re.search(r"[A-Z]", value):
      raise ValidationError('Password must contain at least one capital letter.')
    if not re.search(r"\d", value):
      raise ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
      raise ValidationError("Password must contain at least one special character.")
    
  @post_load(pass_original=True)
  def remove_confirm_password(self, data, orginal_data, **kwargs):
    data.pop('confirm_password')
    return data
  

class LoginSchema(Schema):
  email = fields.Email()
  password = fields.String(required=True, load_only=True)
  remember = fields.Bool()

  @validates('password')
  def validate_password(self, value):
    if len(value) < 8:
      raise ValidationError('Password must have minmum 8 characters length.')
    if not re.search(r"[A-Z]", value):
      raise ValidationError('Password must contain at least one capital letter.')
    if not re.search(r"\d", value):
      raise ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
      raise ValidationError("Password must contain at least one special character.")
