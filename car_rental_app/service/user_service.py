"""
This module consists of the CRUD operations to work with 'user' table
"""
from flask import jsonify
from car_rental_app import db
from ..models.user import User
from ..models.passport import Passport
from log import logger


def create_user(login, name, surname, passport, password):
    """
    Function adding new user
   :param login: user`s login
   :param name: user`s name
   :param surname: user`s surname
   :param passport: passport object
   :param password: user`s password
   :return: None
    """
    try:
        user = User(login=login, name=name, surname=surname, passport=passport, password=password)
        db.session.add(user)
        db.session.commit()
    except:
        logger.error("Can`t add a user to the table")
    return None


def read_all_users():
    """
    Get all users` data from user table by id
    :return: jsonify user data
    """
    try:
        users = User.query.all()
        return jsonify(user_data=[[user.login, user.name, user.surname,
                                   user.passport_id, user.password] for user in users])
    except:
        logger.warning("Can`t get users from db")
    return None


def read_user_by_id(id):
    """
    Get a specific user from table by id
    :param id: user`s id
    :return: data in json format
    """
    try:
        user = User.query.get(id)
        return jsonify([user.login, user.name, user.surname, user.passport_id, user.password])
    except:
        logger.warning("Can`t get a user from db")
    return None


def update_user(id, login=None, name=None, surname=None, password=None):
    """
    Function updating existing user without overwriting the unspecified elements as Null
    :param id: user`s login
    :param login: user`s login
    :param name: user`s name
    :param surname: user`s surname
    :param password: user`s password
    :return: None
    """
    try:
        user = User.query.get_or_404(id)
        if login:
            user.login = login
        elif name:
            user.name = name
        elif surname:
            user.surname = surname
        elif password:
            user.password = password
        db.session.add(user)
        db.session.commit()
    except:
        logger.warning("Can`t update a certain user")
    return None


def update_user_balance(id, balance=None):
    """
    Replenish a specific user balance
    :param id: user`s id
    :param balance: user`s new balance
    :return: None
    """
    try:
        user = User.query.get(id)
        if balance:
            user.balance = balance
    except:
        logger.warning("Can`t update a user`s balance")
    return None


def delete_user(id):
    """
    Delete a specific user and passport data
    :param id: user`s id
    :return: None
    """
    try:
        user = User.query.get_or_404(id)
        passport = Passport.query.filter_by(id=user.passport_id).first()
        db.session.delete(passport)
        db.session.delete(user)
        db.session.commit()
    except:
        logger.warning("Can`t delete a specific user or passport")
    return None
