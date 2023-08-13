from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from models import Task, User

ma = Marshmallow()


class TaskSchema(Schema):

    id = fields.UUID(dump_only=True)
    status = fields.Method("get_status", dump_only=True)
    user_id = fields.String(dump_only=True)
    description = fields.String(required=True)

    def get_status(self, obj):
        return obj.status.value

    class Meta:
        model = Task
        ordered = True


class UserSchema(ma.SQLAlchemySchema):
    id = fields.UUID(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(dump_only=True)
    tasks = ma.auto_field()

    class Meta:
        model = User
        ordered = True


