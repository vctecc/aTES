from flask_marshmallow import Marshmallow
from marshmallow import Schema, ValidationError, fields
from models import Task, User

ma = Marshmallow()


def task_title_validator(title: str):
    if '[' in str:
        raise ValidationError('The name must not contain the JIRA task ID.')


class TaskSchema(Schema):

    public_id = fields.UUID(dump_only=True)
    status = fields.Method("get_status", dump_only=True)
    user_id = fields.String(dump_only=True)
    jura_id = fields.String()
    title = fields.String(required=True, validate=task_title_validator)
    description = fields.String(required=True)

    def get_status(self, obj):
        return obj.status.value

    class Meta:
        model = Task
        ordered = True


class UserSchema(ma.SQLAlchemySchema):
    public_id = fields.UUID(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(dump_only=True)
    tasks = ma.auto_field()

    class Meta:
        model = User
        ordered = True


