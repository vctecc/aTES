from http import HTTPStatus
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from schemas import TaskSchema
from sqlalchemy.sql.expression import func

from models import db, User, Task, UserRoles, TaskStatus


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
            return f"{err.normalized_messages()}", HTTPStatus.BAD_REQUEST

        user = get_random_user()
        if not user:
            return "No users available", HTTPStatus.BAD_REQUEST

        task = Task(description=data['description'], user_id=user.id)
        db.session.add(task)
        db.session.commit()

        resp = jsonify(schema.dump(task))
        resp.status_code = HTTPStatus.CREATED
        return resp


class GetTask(Resource):

    @jwt_required()
    def get(self, task_id: str):
        task_id = db.get_or_404(Task, task_id)
        return jsonify(task_id), HTTPStatus.OK


class ReassignTask(Resource):

    @jwt_required()
    def post(self):
        tasks = db.session.query(Task).filter_by(status=TaskStatus.PROGRESS).all()
        for task in tasks:
            if user := get_random_user():
                task.user = user
                db.session.commit()

        return HTTPStatus.OK
