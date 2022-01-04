"""
Module contains classes to work with REST API for Car.
Class:
    CarListAPI(Resource)
    CarAPI(Resource)
"""
from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from ..models.car import CarSchema
from ..service import car_service

from log import logger


class CarListAPI(Resource):
    """
    Class, which is descendant of Resource.
    It`s responsible for working with all HTTP requests using car_service.
    """

    @staticmethod
    def get():
        """
        Method overrides get method of Resource and works on get method, retrieving all cars and their info.
        :return: dict of users` data
        """
        cars = car_service.read_all_cars()
        cars_data = [car.to_dict() for car in cars]
        return jsonify(cars_data=cars_data, status=200)

    @staticmethod
    def post():
        """
        Method overrides post method of Resource and works on post method, adding cars
        :return: response in json format or error messages
        """
        data = request.get_json()
        if not data:
            return jsonify(message="Fill the data", status=400)
        try:
            CarSchema().load(data)
        except ValidationError as err:
            return jsonify(message=err.messages, status=400)
        name = data["name"]
        model = data["model"]
        year = data["year"]
        price_per_day = data["price_per_day"]
        people_count = data["people_count"]
        try:
            car_service.create_car(name=name,
                                   model=model,
                                   year=year,
                                   price_per_day=price_per_day,
                                   people_count=people_count)
            return jsonify(message="The car was created!", status=201)
        except:
            logger.error(f"Failed to create car.")
            return jsonify(message=f"Wrong data", status=400)


class CarApi(Resource):
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
            car = car_service.read_car_by_id(id)
            if car:
                car_data = car.to_dict()
                return jsonify(car_data=car_data, status=200)
            else:
                return jsonify(message=f"No such car", status=404)
        except AttributeError as e:
            logger.error(f"{e}")
            return jsonify(message=f"{e}", status=400)

    @staticmethod
    def put(id):
        """
        Method overrides put method of Resource and works on put method, editing car by id
        (works as patch, without overwriting old data as Null)
        :return: response in json format or error messages
        """
        data = request.json
        try:
            CarSchema().load(data, partial=True)
        except ValidationError as err:
            return jsonify(message=err.messages, status=400)
        try:
            if car_service.read_car_by_id(id):
                car_service.update_car(id, data)
                return jsonify(message="Car was updated successfully", status=200)
            return jsonify(message="Not valid car id", status=400)
        except:
            logger.error(f"Failed to update car.")
            return jsonify(message=f"Failed to update car", status=400)

    @staticmethod
    def delete(id):
        """
         Method overrides delete method of Resource and works on delete method, deleting car by id
         :return: response in json format or error messages
        """
        try:
            if car_service.read_car_by_id(id):
                car_service.delete_car(id)
                return jsonify(message="Car was deleted successfully", status=200)
            return jsonify(message="Not valid car id", status=400)
        except:
            logger.error(f"Failed to delete car by id")
            return jsonify(message="No such car", status=400)
