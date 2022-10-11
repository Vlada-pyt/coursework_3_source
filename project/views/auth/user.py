from flask_restx import Resource, Namespace
from flask import request
from project.container import user_service
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

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')

        return user_service.get_user_by_token(refresh_token=header)

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}

@api.route('/password/')
class LoginView(Resource):
    def put(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return user_service.update(data=data, refresh_token=header)


@api.route('/<int:bid>')
class UsersView(Resource):
    def get(self, bid):
        b = user_service.get_one(bid)
        sm_d = UserSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204


    def delete(self, bid):
        user_service.delete(bid)
        return "", 204
