from datetime import datetime
from uuid import uuid4

from models import Task
from schemas import TaskSchema


def create_task_event(task: Task) -> dict:
    event = {
        'meta': {
            "id": uuid4(),
            "version": '2',
            "name": 'task.created',
            "time": datetime.now().timestamp(),
        },
        'data': TaskSchema().dump(task)
    }
    return event


def assign_task_event(task: Task) -> dict:
    event = {
        'meta': {
            "id": uuid4(),
            "version": '2',
            "name": 'task.assigned',
            "time": datetime.now().timestamp(),
        },
        'data': TaskSchema().dump(task)
    }
    return event
