from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from flask import request
from http import HTTPStatus
from flask_restful import Resource
from models.user import User
from models.varaus import Varaus
from utils import hash_password
from webargs import fields
from webargs.flaskparser import use_kwargs

from schemas.user import UserSchema
from schemas.varaus import VarausSchema

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))
varaus_list_schema = VarausSchema(many=True)


class UserListResource(Resource):

    def post(self):

        json_data = request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        data, errors = user_schema.load(data=json_data)

        if errors:

            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):

            return{'message': 'Already used Username error'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):

            return{'message': ' Already exist'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)

        user = User(**data)
        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return user_schema.dump(user).data, HTTPStatus.CREATED


class UserResource(Resource):

    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:

            data = user_schema.dump(user).data

        else:

            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK


class MeResource(Resource):

    @jwt_required
    def get(self):

        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dump(user).data, HTTPStatus.OK


class UserVarausListResource(Resource):

    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):

        user = User.get_by_username(username=username)

        if user is None:
            return{'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in['all', 'private']:
            pass
        else:
            visibility = 'public'

        varaukset = Varaus.get_all_by_user(user_id=user.id, visibility=visibility)

        return varaus_list_schema.dump(varaukset).data, HTTPStatus.OK
