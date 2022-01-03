"""
Module contains classes to work with REST API for User.
Class:
    UserListAPI(Resource)
    UserAPI(Resource)
"""
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from ..models.passport import PassportSchema
from ..models.user import User, UserSchema
from ..service import passport_service, user_service

from log import logger
from car_rental_app import bcrypt


class UserListAPI(Resource):
    """
    Class, which is descendant of Resource.
    It`s responsible for working with all HTTP requests using user_service.
    """

    @staticmethod
    def get():
        """
        Method overrides get method of Resource and works on get method, retrieving all users and their passport info.
        :return: dict of users` data
        """
        users_list = user_service.read_all_users()
        user_data = [user.to_dict() for user in users_list]
        return jsonify(users_data=user_data, status=200)

    @staticmethod
    def post():
        """
        Method overrides post method of Resource and works on post method, adding users
        :return: response in json format or error messages
        """
        data = request.get_json()
        if not data:
            return jsonify(message="Fill the data", status=400)
        series = data["series"]
        number = data["number"]
        published_by = data["published_by"]
        date_of_birth = data["date_of_birth"]
        login = data["login"]
        name = data["name"]
        surname = data["surname"]
        password = data["password"]
        password2 = data["repeat_password"]
        try:
            # validation on user & passport schemas
            PassportSchema().load({"series": series,
                                   "number": number,
                                   "published_by": published_by,
                                   "date_of_birth": date_of_birth})

            UserSchema().load({"login": login,
                               "name": name,
                               "surname": surname,
                               "password": password,
                               "password2": password2})
        except ValidationError as err:
            return jsonify(message=err.messages, status=400)
        if User.query.filter_by(login=login).first() is not None:
            return jsonify(message="User with this login is already exist", status=409)
        try:
            # converting to specified data format
            data_to = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            if password != password2:
                return jsonify(message="Passwords aren`t equal", status=400)

            new_passport = passport_service.create_passport(series=series,
                                                            number=number,
                                                            published_by=published_by,
                                                            date_of_birth=data_to)
            if new_passport:
                new_user = user_service.create_user(
                    login=login,
                    name=name,
                    surname=surname,
                    passport=new_passport,
                    password=bcrypt.generate_password_hash(password)
                )
                if not new_user:
                    return jsonify(message="Wrong user data", status=400)
                return jsonify(message="The user was created!", status=201)
            return jsonify(message="Wrong passport data", status=400)
        except (ValueError, KeyError) as e:
            logger.error(f"{e}")
            return jsonify(message=f"{e}", status=400)


class UserApi(Resource):
    """
    Class, which is descendant of Resource.
    It`s responsible for working with all HTTP requests using user_service and existing id.
    """

    @staticmethod
    def get(id):
        """
        Method overrides get method of Resource and works on get method, retrieving user by id.
        :return: dict of user`s data
        """
        try:
            user = user_service.read_user_by_id(id)
            if user:
                user_data = user.to_dict()
                return jsonify(user_data=user_data, status=200)
            else:
                return jsonify(message=f"No such user", status=404)
        except AttributeError as e:
            logger.error(f"{e}")
            return jsonify(message=f"{e}", status=400)

    @staticmethod
    def put(id):
        """
        Method overrides put method of Resource and works on put method, editing users
        :return: response in json format or error messages
        """
        pass

    @staticmethod
    def delete(id):
        """
         Method overrides delete method of Resource and works on delete method, deleting user by id
         :return: response in json format or error messages
        """
        try:
            user_service.delete_user(id)
            return jsonify(message="User was deleted successfully", status=200)
        except:
            logger.error(f"Failed to delete user by id")
            return jsonify(message="No such user", status=400)
