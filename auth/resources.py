from http import HTTPStatus
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from schemas import UserSchema, CreateUserSchema, LoginSchema
from sqlalchemy.exc import IntegrityError

from models import db, User, Role


class UserAPI(Resource):

    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = db.get_or_404(User, identity)
        return jsonify(user)

    @jwt_required()
    def patch(self):
        req = request.get_json(force=True)
        schema = UserSchema()
        try:
            data = schema.load(req, partial=True)
        except ValidationError as err:
            return f"{err.normalized_messages()}", HTTPStatus.BAD_REQUEST

        identity = get_jwt_identity()
        user = db.get_or_404(User, identity)

        for key, value in data.items():
            if key == 'role':
                role = db.session.query(Role).filter(name=value).first()
                user.role = role
            else:
                setattr(user, key, value)
        db.session.commit()

        return jsonify(schema.dump(user))

    def post(self):
        req = request.get_json(force=True)
        schema = CreateUserSchema()
        try:
            data = schema.load(req)
        except ValidationError as err:
            return f"{err.normalized_messages()}", HTTPStatus.BAD_REQUEST

        try:
            role = data.pop('role')
            user = User(**data)
            user.role = db.session.query(Role).filter_by(name=role).first()
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return f"{data['username']} already exists", HTTPStatus.CONFLICT

        access_token = create_access_token(identity=user.id)
        return jsonify(accessToken=access_token)


class AuthAPI(Resource):

    def post(self):
        """
        Returns a JwtTokens object with tokens for authorization in response to the user's transmitted data.
        """
        req = request.get_json(force=True)
        schema = LoginSchema()
        try:
            data = schema.load(req)
        except ValidationError as err:
            return f"{err.normalized_messages()}", HTTPStatus.BAD_REQUEST

        username, password = data["username"], data["password"]
        user = db.session.query(User).filter_by(username=username, password=password).first()
        if not user:
            return "User not found", HTTPStatus.NOT_FOUND

        access_token = create_access_token(user.id)
        return jsonify(accessToken=access_token)
