"""
Module contains classes to work with REST API for Passport.
Class:
    PassportListAPI(Resource)
    PassportAPI(Resource)
"""
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from ..models.passport import Passport, PassportSchema
from ..service import passport_service

from log import logger


class PassportListApi(Resource):
    """
    Class, which is descendant of Resource.
    It`s responsible for working with all HTTP requests using passport_service.
    Available at "/api/passport".
    """

    @staticmethod
    def post():
        """
        Method overrides post method of Resource and works on post method, add new passport
        :return: response in json format or error messages
        """
        data = request.get_json()
        if not data:
            return jsonify(message="Fill the data", status=400)
        series = data["series"]
        number = data["number"]
        published_by = data["published_by"]
        date_of_birth = data["date_of_birth"]
        try:
            PassportSchema().load({"series": series,
                                   "number": number,
                                   "published_by": published_by,
                                   "date_of_birth": date_of_birth})
        except ValidationError as err:
            return jsonify(message=err.messages, status=400)
        if Passport.query.filter_by(number=number).first() is not None:
            return jsonify(message="Passport with this number is already exist", status=409)
        try:
            data_to = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            new_passport = passport_service.create_passport(series=series,
                                                            number=number,
                                                            published_by=published_by,
                                                            date_of_birth=data_to)
            if new_passport:
                return jsonify(message="Passport was created!", status=201)
            return jsonify(message="Passport wasn`t created!", status=400)
        except:
            logger.error(f"Failed to create passport.")
            return jsonify(message=f"Wrong data", status=400)


class PassportApi(Resource):
    """
    Class, which is descendant of Resource.
    It`s responsible for working with all HTTP requests using passport_service and existing id.
    Available at "/api/passport/<id>"
    """

    @staticmethod
    def get(id):
        """
        Method overrides get method of Resource and works on get method, retrieving passport by id.
        :return: dict of passport`s data
        """
        try:
            passport = passport_service.read_passport_by_id(id)
            if passport:
                passport_data = passport.to_dict()
                return jsonify(passport_data=passport_data, status=200)
            else:
                return jsonify(message=f"No such passport in db", status=404)
        except AttributeError as e:
            logger.error(f"{e}")
            return jsonify(message=f"{e}", status=400)

    @staticmethod
    def put(id):
        """
        Method overrides put method of Resource and works on put method, editing passport
        :return: response in json format or error messages
        """
        pass
