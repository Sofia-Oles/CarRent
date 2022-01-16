import unittest
from datetime import date

from car_rental_app.tests.base import BaseTestCase

from car_rental_app import db
from car_rental_app.models.user import User
from car_rental_app.models.passport import Passport
from car_rental_app.service import user_service, passport_service

test_passport = {
    "series": "KC",
    "number": 22899239,
    "published_by": 4920,
    "date_of_birth": date.fromisoformat("2001-12-04"),
}
test_user = {
    "login": "test_user@gmail.com",
    "name": "Ivan",
    "surname": "Ivanov",
    "password": "12345super",
}


class TestUserService(BaseTestCase):
    def test_create_user(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        if passport:
            user = user_service.create_user(passport=passport, **test_user)
        self.assertEqual(1, User.query.count())

    def test_read_all_users(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        user = User(passport=passport, **test_user)
        db.session.add(user)
        db.session.commit()
        self.assertEqual(1, len(user_service.read_all_users()))

    def test_read_user(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        user = User(passport=passport, **test_user)
        db.session.add(user)
        db.session.commit()
        user_from_db = user_service.read_user_by_id(1)
        self.assertEqual(1, user_from_db.id)

    def test_update_user(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        user = User(passport=passport, **test_user)
        db.session.add(user)
        db.session.commit()
        old_data = user.to_dict()
        data_to_update = {"name": "UPDATED", "login": "super@gmail.com"}
        user_service.update_user(1, data_to_update)
        self.assertNotEqual(old_data["name"], User.query.get(1).name)
        self.assertNotEqual(old_data["login"], User.query.get(1).login)

    def test_update_user_balance(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        user = User(passport=passport, **test_user)
        db.session.add(user)
        db.session.commit()
        old_data = user.to_dict()
        user_service.update_user_balance(1, 4000)
        self.assertNotEqual(old_data["balance"], User.query.get(1).balance)

    def test_delete_user(self):
        passport = Passport(**test_passport)
        db.session.add(passport)
        db.session.commit()
        user = User(passport=passport, **test_user)
        db.session.add(user)
        db.session.commit()
        user_service.delete_user(1)
        self.assertEqual(0, User.query.count())
        self.assertEqual(0, Passport.query.count())


if __name__ == "__main__":
    unittest.main()
