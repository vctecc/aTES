from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from models import Task, Account, User

ma = Marshmallow()


class BaseSchema(Schema):
    public_id = fields.UUID(dump_only=True)


class AccountSchema(BaseSchema):

    class Meta:
        model = Account
        ordered = True


class UserSchema(BaseSchema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(dump_only=True)

    class Meta:
        model = User
        ordered = True


class TaskSchema(BaseSchema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(dump_only=True)

    class Meta:
        model = Task
        ordered = True
