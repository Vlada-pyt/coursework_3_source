from flask_restx import Resource, Namespace
from flask import request
from project.container import user_service
from project.decorators import auth_required
from project.models import UserSchema

from project.setup.api.models import user

api = Namespace('users')

@api.route('/')
class UsersView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK' )
    def patch(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return user_service.update_user(data=data, refresh_token=header)


    def get(self):

        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        return UserSchema().dump(user_service.get_user_by_token(refresh_token=header))

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}

@api.route('/password/')
class LoginView(Resource):
    @auth_required
    def put(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return user_service.update_password(data=data, refresh_token=header)


