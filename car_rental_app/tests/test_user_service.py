import unittest
from car_rental_app.tests.base import BaseTestCase

from car_rental_app import db
from car_rental_app.models.user import User
from car_rental_app.service import user_service, passport_service


class TestUserService(BaseTestCase):
    def test_read_all_users(self):
        user = User(
            login="user222@gmail.com",
            name="Ivan",
            surname="Ivanov",
            passport_id=5,
            password="12345",
        )
        db.session.add(user)
        db.session.commit()
        self.assertEqual(1, len(user_service.read_all_users()))


if __name__ == "__main__":
    unittest.main()
