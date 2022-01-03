"""
This module consists of the CRUD operations to work with 'car' table
"""
from flask import jsonify
from car_rental_app import db
from ..models.car import Car
from log import logger


# admin
def create_car(name, model, year, price_per_day, people_count):
    """
    Function adding new employee to specific department
   :param name: car`s name
   :param model: car`s model
   :param year: car`s year of production
   :param price_per_day: car`s price for rent
   :param people_count: car`s capacity
   :return: None
    """
    try:
        car = Car(name=name, model=model, year=year, price_per_day=price_per_day, people_count=people_count)
        db.session.add(car)
        db.session.commit()
    except:
        logger.warning("Can`t create a car")
    return None


# for both admin and user
def read_all_cars():
    """
    Select all records from car table
    :return: the list of all cars in json
    """
    try:
        cars = Car.query.all()
        return cars
    except:
        logger.warning("Can`t get cars from db")
    return None


# both
def read_car_by_id(id):
    """
    Get a specific car from car table by id
    :param id: car`s id
    :return: data in json format
    """
    try:
        car = Car.query.get(id)
        return car
    except:
        logger.warning("Can`t get a car from db")
    return None


# admin
def update_car(id, data):
    """
    Update an existing car without overwriting the unspecified elements as Null
    :param id: car`s id
    :param data: data to change
    :return: None
    """
    try:
        db.session.query(Car).filter_by(id=id).update(data)
        db.session.commit()
    except:
        logger.warning("Can`t update a certain car")
    return None


# admin
def delete_car(id):
    """
    Delete an existing car
    :param id: id by which the required car is deleted
    """
    try:
        car = Car.query.get(id)
        db.session.delete(car)
        db.session.commit()
    except:
        logger.warning("Can`t delete a specific car")
    return None
