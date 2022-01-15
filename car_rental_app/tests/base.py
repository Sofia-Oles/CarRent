"""
This module defines the BaseTestCase class
"""
import unittest
from car_rental_app import create_app, db


class BaseTestCase(unittest.TestCase):
    """
    Base test case class
    """

    def setUp(self):
        """
        Execute before every test case
        """
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Execute after every test case
        """
        # pass
        db.session.remove()
        db.drop_all()
