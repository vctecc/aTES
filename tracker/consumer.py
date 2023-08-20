import json
import time

from app import create_app
from flask import Flask
from loguru import logger
from models import User, db
from streams import RedisStream, user_stream
from config import Config
from schema_registry import SchemaRegistry, ValidationError

schema_registry = SchemaRegistry(Config)


def database_loader(app: Flask, msg_data: dict) -> None:
    with app.app_context():
        try:
            schema_registry.validate(msg_data, 'user.created', 1)
        except ValidationError:
            logger.error('Unsupported streaming data')
            # TODO save in DataBase
            return None

        operation = msg_data['meta']['name']
        data = msg_data['data']
        if operation == 'user.created':
            user = User(**data)
            db.session.add(user)
        elif operation == 'user.updated':
            user = db.session.query(User).get(['id'])
            for key, value in data.items():
                setattr(user, key, value)

        db.session.commit()
        return None


def stream_producer(stream: RedisStream):
    while True:
        if data := stream.read():
            for msg in data:
                yield json.loads(msg[1]['msg'])
        else:
            time.sleep(1)


def processing(app: Flask, stream: RedisStream):
    for msg in stream_producer(stream):
        database_loader(app, msg)


if __name__ == "__main__":
    tracker_app = create_app('config.Config')
    processing(tracker_app, user_stream)
