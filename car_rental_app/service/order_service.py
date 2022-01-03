"""
This module consists of the CRUD operations to work with 'order' table
"""
from flask import jsonify
from car_rental_app import db
from ..models.order import Order
from ..models.user import User
from ..models.car import Car
from log import logger


def create_order(creator, car, start_date, end_date, price):
    """
    Function of creation a new order
    :param creator: backref to user
    :param car: backref to car
    :param start_date: date of rent start
    :param end_date: date of rent end
    :param price: total price
    :return: None
    """
    try:
        user = User.query.get(creator.id)
        car = Car.query.get(car.id)
        order = Order(creator=user, car=car, start_date=start_date, end_date=end_date, price=price)
        db.session.add(order)
        db.session.commit()
    except:
        logger.warning("Can`t find such user or car to create an order!")
    return None


def read_all_orders():
    """
    Select all records from order table
    :return: the list of all order in json
    """
    try:
        orders = Order.query.all()
        return jsonify(all_orders=[[i.creator, i.car, i.start_date, i.end_date, i.price] for i in orders])
    except:
        logger.warning("Can`t get orders from db")
    return None


def read_order_by_id(id):
    """
    Get a specific order from order table by id
    :param id: order`s id
    :return: data in json format
    """
    try:
        order = Order.query.get(id)
        return jsonify([order.creator, order.car, order.start_date, order.end_date, order.price])
    except:
        logger.warning("Can`t get an order from db")
    return None


def delete_order(id):
    """
    Delete a specific order
    :param id: user`s id
    :return: None
    """
    try:
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
    except:
        logger.warning("Can`t delete a specific order")
    return None
