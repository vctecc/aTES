from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from models import User

ma = Marshmallow()


def convert_to_camelcase(s: str):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class BaseSchema(ma.Schema):

    def on_bind_field(self, field_name: str, field: fields.Field):
        field.data_key = convert_to_camelcase(field.data_key or field_name)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class CreateUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)


class UserSchema(BaseSchema):

    public_id = fields.UUID(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(dump_only=True)

    class Meta:
        model = User
        ordered = True
