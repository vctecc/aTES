import json
from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource
from marshmallow import ValidationError
from models import Role, User, db
from schemas import CreateUserSchema, LoginSchema, UserSchema
from sqlalchemy.exc import IntegrityError
from streams import user_stream


class UserAPI(Resource):

    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        if user := db.session.query(User).filter_by(public_id=identity).first():
            return jsonify(UserSchema().dump(user))
        return HTTPStatus.NOT_FOUND

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
        # TODO sed message to broker
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

            # TODO use special functional for that
            msg = {
                'operation': 'created',
                'data': {
                    'public_id': user.public_id,
                    'role': user.role.name,
                    'username': user.username,
                    'email': user.email
                }
            }
            user_stream.save({'msg': json.dumps(msg)})

        except IntegrityError:
            return f"{data['username']} already exists", HTTPStatus.CONFLICT

        access_token = create_access_token(identity=user.public_id)
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

        access_token = create_access_token(user.public_id)
        return jsonify(accessToken=access_token)
