from datetime import datetime
from uuid import uuid4

from models import User
from schemas import UserSchema


def create_user_event(user: User) -> dict:
    event = {
        'meta': {
            "id": uuid4(),
            "version": '1',
            "name": 'user.created',
            "time": datetime.now().timestamp(),
        },
        'data': UserSchema().dump(user)
    }
    return event


def update_user_event(user: User) -> dict:
    event = {
        'meta': {
            "id": uuid4(),
            "version": '1',
            "name": 'user.updated',
            "time": datetime.now().timestamp(),
        },
        'data': UserSchema().dump(user)
    }
    return event