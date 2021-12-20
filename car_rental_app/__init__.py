from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash
from flask_marshmallow import Marshmallow
# from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_restful import Api
from config import Configuration


db = SQLAlchemy()
ma = Marshmallow()
# login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    """
    Create flask application
    :return: the created flask application
    """
    app = Flask(__name__)
    app.config.from_object(Configuration)

    from .views import public_blueprint
    app.register_blueprint(public_blueprint)

    from car_rental_app import models

    db.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()



    # login_manager.init_app(app)
    #
    # Migrate(app, db)

    # from .rest import employee_api, department_api

    # api = Api(app)

    # api.add_resource(department_api.DepartmentListApi, '/api/departments')
    # api.add_resource(department_api.Department, '/api/departments/<id>')
    #
    # # adding the employee resources
    # api.add_resource(employee_api.EmployeeListApi, '/api/employees')
    # api.add_resource(employee_api.Employee, '/api/employees/<id>')


    return app
