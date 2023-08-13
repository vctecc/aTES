from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from models import Role, User, db
from resources import AuthAPI, UserAPI


def create_app(config_filename: str):
    app = Flask("auth")
    app.config.from_object(config_filename)

    db.init_app(app)
    models = (User, Role)

    api = Api()
    api.resources.clear()
    api.add_resource(UserAPI, "/api/user")
    api.add_resource(AuthAPI, "/api/auth")

    api.init_app(app) # noqa

    migrate = Migrate()
    migrate.init_app(app, db)

    jwt = JWTManager()
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        for role in ('admin', 'developer', 'manager'):
            db.session.add(Role(name=role))
        db.session.commit()
    return app


if __name__ == "__main__":
    app = create_app('config.Config')
    app.run()
