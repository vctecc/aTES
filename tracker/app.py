from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db


def create_app(config_filename: str):
    app = Flask("tracker")
    app.config.from_object(config_filename)

    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    api = Api()
    api.init_app(app)

    jwt = JWTManager()
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app
