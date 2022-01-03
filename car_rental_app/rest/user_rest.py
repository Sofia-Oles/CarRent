"""
Module contains classes to work with REST API for User.
Class:
    UserAPI(Resource) uses user_service
"""
from datetime import date, datetime
from flask import redirect, jsonify, request
from flask_restful import Resource, abort, reqparse
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
        :return: dict of users data in json format
        """
        users_list = user_service.read_all_users()
        user_data = [user.to_dict() for user in users_list]
        return jsonify(users_data=user_data)

    # {"series": "MC", "number": 226099823, "published_by": 4622, "date_of_birth": "2001-12-22",
    #  "login": "user222@gmail.com", "name": "ckk", "surname": "NOTE7", "password": "12345", "repeat_password":
    #      "12345"}
    @staticmethod
    def post():
        """
        Method overrides post method of Resource and works on post method, adding users
        :return: response in json format or error messages
        """
        data = request.get_json()
        if not data:
            return jsonify(message="Fill the data", status=400)
        try:
            # I validate USER & PASSPORT for not empty or ''
            PassportSchema().load({"series": data["series"],
                                   "number": data["number"],
                                   "published_by": data["published_by"],
                                   "date_of_birth": data["date_of_birth"]})

            UserSchema().load({"login": data["login"], "name": data["name"],
                               "surname": data["surname"], "password": data["password"],
                               "password2": data["repeat_password"]})
        except ValidationError as err:
            return jsonify(message=err.messages, status=400)

        try:
            # converting to specified data format
            date_of_birth = data["date_of_birth"]
            data_to = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

            if data["password"] != data["repeat_password"]:
                return jsonify(message="Passwords aren`t equal", status=400)

            new_passport = passport_service.create_passport(series=data["series"], number=data["number"],
                                                            published_by=data["published_by"], date_of_birth=data_to)

            if new_passport:
                if User.query.filter_by(login=data["login"]).first() is not None:
                    return jsonify(message="User with this login is already exist", status=409)

                new_user = user_service.create_user(
                    login=data["login"],
                    name=data["name"],
                    surname=data["surname"],
                    passport=new_passport,
                    password=bcrypt.generate_password_hash(data["password"])
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
        :return: dict of users data in json format
        """
        try:
            user = user_service.read_user_by_id(id)
            user_data = user.to_dict()
            return jsonify(user_data=user_data, status=200)
        except AttributeError as e:
            logger.error(f"{e}")
            return jsonify(message=f"{e}", status=400)

    @staticmethod
    def put(id):
        """
        Method overrides put method of Resource and works on put method, editing users
        :return: response in json format or error messages
        """
        #
        # login = args['login']
        # password = args['password']
        # user = User.query.filter_by(login=login).first()
        # new_login = args['new_login']
        # new_password = args['new_password']
        # id = args['id']
        # page = args.get('page')
        # if user and user.id == 1 and user.password == password:
        #     if check_empty_strings(new_login, new_password) and User.query.get(id) \
        #             and (not User.query.filter_by(login=new_login).first() or User.query.get(id).login == new_login):
        #         change_user(id, new_login, new_password)
        #         logger.info(f'Edited user: id: "{id}" new_login: "{new_login}"\tnew_password: "{new_password}"')
        #         if page and page == 'True':
        #             return redirect('/users')
        #         return {'message': 'EDIT_SUCCESS'}
        #     logger.info(f'Edited user: id: "{id}" new_login: "{new_login}"\tnew_password: "{new_password}"')
        #     if page and page == 'True':
        #         return redirect('/users')
        #     abort(401, error='VALUES_INCORRECT')
        # logger.info(f'Failed editing user: "{login}"\tpassword: "{password}"')
        # abort(401, error='CREDENTIALS_INCORRECT')

    @staticmethod
    def delete(id):
        """
         Method overrides delete method of Resource and works on delete method, deleting user by id
         :return: messages or errors
        """
        user = user_service.read_user_by_id(id)
        if user:
            user_service.delete_user(id)
            return jsonify(message="User was deleted successfully", status=200)
        return jsonify(message="No such user", status=400)
