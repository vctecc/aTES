from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db, Task, User
from resources import CreateTask, GetTask, ReassignTask


def create_app(config_filename: str):
    app = Flask("tracker")
    app.config.from_object(config_filename)

    db.init_app(app)
    models = (User, Task)

    api = Api()
    api.resources.clear()
    api.add_resource(GetTask, "/api/task/<task_id>")
    api.add_resource(CreateTask, "/api/task")
    api.add_resource(ReassignTask, "/api/reassign")

    api.init_app(app)  # noqa

    migrate = Migrate()
    migrate.init_app(app, db)

    jwt = JWTManager()
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        user = User(username='FirstPopug', email='fist_popug@popug.io')
        db.session.add(user)
        db.session.commit()
    return app


if __name__ == "__main__":
    app = create_app('config.Config')
    app.run(port=5001)
