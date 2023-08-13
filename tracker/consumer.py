import json
import time

from app import create_app
from flask import Flask
from models import User, db
from streams import RedisStream, user_stream


def database_loader(app: Flask, msg: dict):
    with app.app_context():
        operation = msg['operation']
        data = msg['data']
        if operation == 'created':
            user = User(**data)
            db.session.add(user)
        elif operation == 'updated':
            user = db.session.query(User).get(['id'])
            for key, value in data.items():
                setattr(user, key, value)

        db.session.commit()


def stream_producer(stream: RedisStream):
    while True:
        if data := stream.read():
            for msg in data:
                print(msg)
                yield json.loads(msg[1]['msg'])
        else:
            time.sleep(1)


def processing(app: Flask, stream: RedisStream):
    for msg in stream_producer(stream):
        database_loader(app, msg)


if __name__ == "__main__":
    tracker_app = create_app('config.Config')
    processing(tracker_app, user_stream)
