import unittest

from car_rental_app import db
from car_rental_app.models.user import User
from car_rental_app.service import user_service, passport_service, car_service
from car_rental_app.tests.base import BaseTestCase


class TestUserService(BaseTestCase):

    def test_get_all_departments(self):
        pass1 = car_service.create_car( name="Land Cruiser", model="DF6732", year=2017, price_per_day=100, people_count=6)
        self.assertEqual(1, len(car_service.read_all_cars()))


if __name__ == "__main__":
    unittest.main()
