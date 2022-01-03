"""
Module contains classes to work with REST API, API instance.
Classes:

"""
from flask_restful import Api
from .user_rest import UserListAPI, UserApi

r_api = Api()

r_api.add_resource(UserListAPI, "/api/users")
r_api.add_resource(UserApi, "/api/users/<id>")



