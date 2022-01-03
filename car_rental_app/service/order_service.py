"""
This module consists of the CRUD operations to work with 'order' table
"""
from flask import jsonify
from sqlalchemy import extract

from car_rental_app import db
from ..models.order import Order
from ..models.user import User
from ..models.car import Car
from log import logger


def create_order(user_id, car_id, start_date, end_date, price):
    """
    Function of creation a new order
    :param user_id: user id
    :param car_id: car id
    :param start_date: date of rent start
    :param end_date: date of rent end
    :param price: total price
    :return: None
    """
    try:
        user = User.query.get(user_id)
        car = Car.query.get(car_id)
        order = Order(creator=user, car=car, start_date=start_date, end_date=end_date, price=price)
        db.session.add(order)
        db.session.commit()
        return order
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
        return orders
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
        return order
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


def retrieve_busy_dates(car_id, start_date, end_date):
    """
    Read all orders with specific car_id and dates
    :param car_id: car`s id
    :param start_date: order`s start date
    :param end_date: orders`s end date
    :return: set of busy orders
    """
    try:
        busy_start = Order.query.filter(
            extract("month", Order.start_date) <= start_date.month,
            extract("month", Order.end_date) >= start_date.month,
            extract("year", Order.start_date) <= start_date.year,
            extract("year", Order.end_date) >= start_date.year,
            extract("day", Order.start_date) <= start_date.day,
            extract("day", Order.end_date) >= start_date.day).filter_by(car_id=car_id).all()

        busy_end = Order.query.filter(
            extract("month", Order.start_date) <= end_date.month,
            extract("month", Order.end_date) >= end_date.month,
            extract("year", Order.start_date) <= end_date.year,
            extract("year", Order.end_date) >= end_date.year,
            extract("day", Order.start_date) <= end_date.day,
            extract("day", Order.end_date) >= end_date.day).filter_by(car_id=car_id).all()
        busy = set(busy_start + busy_end)
        return busy
    except:
        logger.warning("Can`t delete a specific order")
    return None
