from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow

from models import Task

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


