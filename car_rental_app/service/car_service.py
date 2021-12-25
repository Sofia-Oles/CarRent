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
    :return: the list of all cars
    """
    try:
        cars = Car.query.all()
        return jsonify(all_cars=[[i.name, i.model, i.year, i.price_per_day, i.people_count] for i in cars])
    except:
        logger.warning("Can`t get cars from db")
    return None


# both
def read_car_by_id(id):
    """
    Get a specific car from car table by id
    :param id: car`s id
    :return: car object with a special id
    """
    try:
        car = Car.query.get(id)
        return jsonify([car.name, car.model, car.year, car.price_per_day, car.people_count])
    except:
        logger.warning("Can`t get a car from db")
    return None


# admin
def update_car(id, name=None, model=None, year=None, price_per_day=None, people_count=None):
    """
    Update an existing car without overwriting the unspecified elements as Null
    :param name: car`s name
    :param model: car`s model
    :param year: car`s year of production
    :param price_per_day: car`s price for rent
    :param people_count: car`s capacity
    :return: None
    """
    try:
        car = Car.query.get_or_404(id)
        if name:
            car.name = name
        elif model:
            car.model = model
        elif year:
            car.year = year
        elif price_per_day:
            car.price_per_day = price_per_day
        elif people_count:
            car.people_count = people_count
        db.session.add(car)
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
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()