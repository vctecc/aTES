from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db


def create_app(config_filename: str):
    app = Flask("auth")
    app.config.from_object(config_filename)

    db.init_app(app)

    api = Api()
    api.resources.clear()
    api.init_app(app) # noqa

    migrate = Migrate()
    migrate.init_app(app, db)

    jwt = JWTManager()
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app
