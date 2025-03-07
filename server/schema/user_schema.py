from marshmallow import Schema, validate, validates, ValidationError, fields, post_load, validates_schema
import re
import os

ROLE_TYPES = ['ADMIN', 'MODIRATOR', 'USER']
PERMISSION_TYPES = ['R','W','RW','RWD']

class RoleSchema(Schema):
  role = fields.String(
    required=True, 
    validate=validate.OneOf(
      ROLE_TYPES, 
      error="Invaild role. Allowed values: "+", ".join(ROLE_TYPES)
    )
  )
  premission = fields.String(
    required=True,
    validate=validate.OneOf(
      PERMISSION_TYPES,
      error="Invaild permission. Allowed values: "+", ".join(PERMISSION_TYPES)
    )
  )

class RegisterSchema(Schema):
  id = fields.String(dump_only=True)
  username = fields.String(validate=validate.Length(min=2, max=20), required=True)
  password = fields.String(required=True, load_only=True)
  confirm_password = fields.String(required=True, load_only=True)
  email = fields.Email()
  role = fields.Nested(RoleSchema, load_default=lambda: {"role": "USER", "permission": "R"})

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
    
  @validates_schema
  def validate(self, data, **kwarges):
    if data.get('password') != data.get('confirm_password'):
      raise ValidationError('Password must match', field_name=['confirm_password'])
    
  @post_load(pass_original=True)
  def remove_confirm_password(self, data, orginal_data, **kwargs):
    data.pop('confirm_password')
    return data
  

class LoginSchema(Schema):
  email = fields.Email(required=True)
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

class UpdateAccountSchema(Schema):
  username = fields.String()
  image = fields.Raw()

  @validates('image')
  def validate_image(self, value):
    if not hasattr(value, 'filename'):
      raise ValueError("Invalid file object.")
    
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
    _, ext = os.path.splitext(value.filename)
    if ext.lower() not in allowed_extensions:
      raise ValidationError(f"File type '{ext}' not allowed.")
    
    value.seek(0, os.SEEK_END)
    size = value.tell()
    value.seek(0)
    max_size = 5 * 1024 * 1024
    if size > max_size:
      raise ValidationError("File is too large. Maximum size is 5MB")