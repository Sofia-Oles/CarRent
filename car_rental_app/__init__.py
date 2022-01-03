from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash
from flask_marshmallow import Marshmallow
# from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from config import Configuration


db = SQLAlchemy()
ma = Marshmallow()
# login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():
    """
    Create flask application
    :return: the created flask application
    """
    app = Flask(__name__)
    app.config.from_object(Configuration)

    from .views import public_blueprint
    app.register_blueprint(public_blueprint)

    db.init_app(app)
    bcrypt.init_app(app)
    # with app.app_context():
    #     db.create_all()

    # login_manager.init_app(app)

    from car_rental_app import models
    migrate.init_app(app, db)

    from .views import public_blueprint
    app.register_blueprint(public_blueprint)

    from .rest import r_api
    r_api.init_app(app) # Calling Api.init_app() is not required here because registering the blueprint with the app takes care of setting up the routing for the application

    return app
