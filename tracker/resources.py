from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource
from marshmallow import ValidationError
from models import Task, TaskStatus, User, UserRoles, db
from schemas import TaskSchema, UserSchema
from sqlalchemy.sql.expression import func


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

        return HTTPStatus.OK


class GetUser(Resource):

    @jwt_required()
    def get(self, user_id: str):
        if user := db.session.query(User).filter_by(public_id=user_id).first():
            return jsonify(UserSchema().dump(user))
        return HTTPStatus.NOT_FOUND
