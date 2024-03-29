"""
Module contains classes to work with REST API, API instance.
Classes:

"""
from flask_restful import Api
from .user_rest import UserListAPI, UserApi
from .passport_rest import PassportListApi, PassportApi
from .car_rest import CarListAPI, CarApi
from .order_rest import OrderListAPI, OrderApi

r_api = Api()

r_api.add_resource(UserListAPI, "/api/users")
r_api.add_resource(UserApi, "/api/user/<id>")

r_api.add_resource(PassportListApi, "/api/passport")
r_api.add_resource(PassportApi, "/api/passport/<id>")

r_api.add_resource(CarListAPI, "/api/cars")
r_api.add_resource(CarApi, "/api/car/<id>")

r_api.add_resource(OrderListAPI, "/api/orders")
r_api.add_resource(OrderApi, "/api/order/<id>")
