"""
This module consists of the CRUD operations to work with 'passport' table
"""
from car_rental_app import db
from ..models.passport import Passport
from log import logger

# actions by user


def create_passport(series, number, published_by, date_of_birth):
    """
    Function adding new passport data
   :param series: passport series
   :param number: passport number
   :param published_by: number of department, which published passport
   :param date_of_birth: user`s date of birth
   :return: None
    """
    try:
        passport = Passport(series=series, number=number, published_by=published_by, date_of_birth=date_of_birth)
        db.session.add(passport)
        db.session.commit()
        return passport
    except:
        logger.warning("Can`t add a passport to the table")
    return None


def read_passport_by_id(id):
    """
    Get a specific passport data from passport table by id
    :param id: id of passport
    :return: object with a special id // None
    """
    try:
        passport = Passport.query.get(id)
        return passport
    except:
        logger.warning("Can`t get a specific passport from db")
    return None


def update_passport(id, series=None, number=None, published_by=None, date_of_birth=None):
    """
    Update an existing passport without overwriting the unspecified elements as Null
    :param id: id
    :param series: passport series
    :param number: passport number
    :param published_by: number of department, which published passport
    :param date_of_birth: user`s date of birth
    :return: None
    """
    try:
        passport = Passport.query.get(id)
        if series:
            passport.series = series
        elif number:
            passport.number = number
        elif published_by:
            passport.published_by = published_by
        elif date_of_birth:
            passport.date_of_birth = date_of_birth
        db.session.add(passport)
        db.session.commit()
    except:
        logger.warning("Can`t update a certain passport")
    return None
