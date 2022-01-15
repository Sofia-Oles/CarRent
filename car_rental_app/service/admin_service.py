"""
This module consists of the CRUD operations to work with 'admin' table
"""
from car_rental_app import db
from ..models.administrator import Administrator


def update_balance(price):
    admin = Administrator.query.get(1)
    old = admin.balance
    admin.balance = old + price
    db.session.commit()
