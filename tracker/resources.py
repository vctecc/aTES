from http import HTTPStatus

from events import assign_task_event, create_task_event
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from models import Task, TaskStatus, User, UserRoles, db
from schemas import TaskSchema, UserSchema
from sqlalchemy.sql.expression import func
from streams import task_stream


def get_random_user() -> User | None:
    return db.session.query(User).filter_by(role=UserRoles.DEVELOPER).order_by(func.random()).first()


class CreateTask(Resource):

    @jwt_required()
    def post(self):
        req = request.get_json(force=True)
        schema = TaskSchema()

        try:
            data = schema.load(req)
        except ValidationError as err:
            print(err.normalized_messages())
            return f"{err.normalized_messages()}", HTTPStatus.BAD_REQUEST

        user = get_random_user()
        if not user:
            print("No users available")
            return "No users available", HTTPStatus.BAD_REQUEST

        task = Task(description=data['description'], user_id=user.public_id)
        db.session.add(task)
        db.session.commit()

        task_stream.send(create_task_event(task))

        resp = jsonify(schema.dump(task))
        resp.status_code = HTTPStatus.CREATED
        return resp


class GetTask(Resource):

    @jwt_required()
    def get(self, task_id: str):
        if task := db.session.query(Task).filter_by(public_id=task_id).first():
            return jsonify(task), HTTPStatus.OK


class ReassignTask(Resource):

    @jwt_required()
    def post(self):
        tasks = db.session.query(Task).filter_by(status=TaskStatus.PROGRESS).all()
        for task in tasks:
            if user := get_random_user():
                task.user = user
                db.session.commit()
                task_stream.send(assign_task_event(task))

        return HTTPStatus.OK


class GetUser(Resource):

    @jwt_required()
    def get(self, user_id: str):
        if user := db.session.query(User).filter_by(public_id=user_id).first():
            return jsonify(UserSchema().dump(user))
        return HTTPStatus.NOT_FOUND
