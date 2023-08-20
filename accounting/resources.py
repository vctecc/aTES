from http import HTTPStatus

from events import assign_task_event, create_task_event
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from models import Task, TaskStatus, User, UserRoles, db, Account
from schemas import TaskSchema, UserSchema, AccountSchema
from sqlalchemy.sql.expression import func
from streams import task_stream


class UserView(Resource):

    @jwt_required()
    def get(self, user_id: str):
        if user := db.session.query(User).filter_by(public_id=user_id).first():
            return jsonify(UserSchema().dump(user))
        return HTTPStatus.NOT_FOUND


class AccountView(Resource):

    @jwt_required()
    def get(self, account_id: str):
        if account := db.session.query(Account).filter_by(public_id=account_id).first():
            return jsonify(AccountSchema().dump(account))
        return HTTPStatus.NOT_FOUND


class AccountListView(Resource):

    @jwt_required()
    def get(self):
        accounts = db.session.query(Account).all()
        return jsonify(AccountSchema().dump(accounts))


class StatisticsView(Resource):

    @jwt_required()
    def get(self, account_id: str):
        ...

