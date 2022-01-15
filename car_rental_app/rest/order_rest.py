"""
Module contains classes to work with REST API for Order.
Class:
    OrderListAPI(Resource)
    OrderAPI(Resource)
"""
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource

from ..service import order_service

from log import logger


class OrderListAPI(Resource):
    """
    Class, which is descendant of Resource.
    It`s responsible for working with all HTTP requests using order_service.
    """

    @staticmethod
    def get():
        """
        Method overrides get method of Resource and works on get method, retrieving all orders and their info.
        :return: dict of orders` data
        """
        orders = order_service.read_all_orders()
        orders_data = [order.to_dict() for order in orders]
        return jsonify(orders_data=orders_data, status=200)

    @staticmethod
    def post():
        """
        Method overrides post method of Resource and works on post method, adding cars
        :return: response in json format or error messages
        """
        data = request.get_json()
        if not data:
            return jsonify(message="Fill the data", status=400)
        user_id = data["user_id"]
        car_id = data["car_id"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        price = data["price"]

        # parse to format
        try:
            start_date = datetime.fromisoformat(start_date).replace(hour=9, minute=00)
            end_date = datetime.fromisoformat(end_date).replace(hour=9, minute=00)
        except Exception as e:
            logger.error(f"Failed to create order, {e}")
            return jsonify(message=f"{e}", status=400)
        try:
            # check if dates is available
            orders = order_service.retrieve_busy_dates(car_id, start_date, end_date)
            if not orders:
                order_service.create_order(user_id=user_id,
                                           car_id=car_id,
                                           start_date=start_date,
                                           end_date=end_date,
                                           price=price)
                return jsonify(message="The order was created!", status=201)
            return jsonify(message="Choose another dates!", status=400)
        except:
            logger.error(f"Failed to create order.")
            return jsonify(message=f"Wrong data", status=400)


class OrderApi(Resource):
    """
    Class, which is descendant of Resource.
    It`s responsible for working with all HTTP requests using order_service and existing id.
    """

    @staticmethod
    def get(id):
        """
        Method overrides get method of Resource and works on get method, retrieving order by id.
        :return: dict of user`s data
        """
        try:
            order = order_service.read_order_by_id(id)
            if order:
                order_data = order.to_dict()
                return jsonify(car_data=order_data, status=200)
            else:
                return jsonify(message=f"No such order", status=404)
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
            data["start_date"] = datetime.fromisoformat(data["start_date"]).replace(
                hour=9, minute=00
            )
            data["end_date"] = datetime.fromisoformat(data["end_date"]).replace(
                hour=9, minute=00
            )
        except Exception as e:
            logger.error(f"Failed to create order, {e}")
            return jsonify(message=f"No {e}", status=400)
        try:
            if order_service.read_order_by_id(id):
                order_service.update_order(id, data)
                return jsonify(message="Order was updated successfully", status=200)
            return jsonify(message="Not valid order id", status=400)
        except:
            logger.error(f"Failed to update order.")
            return jsonify(message=f"Failed to update order", status=400)

    @staticmethod
    def delete(id):
        """
        Method overrides delete method of Resource and works on delete method, deleting order by id
        :return: response in json format or error messages
        """
        try:
            if order_service.read_order_by_id(id):
                order_service.delete_order(id)
                return jsonify(message="Order was deleted successfully", status=200)
            return jsonify(message="Not valid order id", status=400)
        except:
            logger.error(f"Failed to delete order by id")
            return jsonify(message="No such order", status=400)
