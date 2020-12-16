from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.huoneet import Huoneet

from schemas.huoneet import HuoneetSchema

huoneet_schema = HuoneetSchema()
huoneet_list_schema = HuoneetSchema(many=True)


class HuoneListResource(Resource):

    def get(self):

        huoneetkin = Huoneet.get_all_huoneet()

        return huoneet_list_schema.dump(huoneetkin).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()

        data, errors = huoneet_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        huone = Huoneet(**data)
        huone.user_id = current_user
        huone.save()

        return huoneet_schema.dump(huone).data, HTTPStatus.CREATED


class HuoneetResource(Resource):

    def get(self, huone_id):

        huone = Huoneet.get_by_id(huone_id=huone_id)

        if huone is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        return huone.data(), HTTPStatus.OK

    @jwt_required
    def put(self, huone_id):

        json_data = request.get_json()

        huone = Huoneet.get_by_id(huone_id=huone_id)

        if huone is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        huone.name = json_data['name']

        huone.save()

        return huone.data(), HTTPStatus

    @jwt_required
    def patch(self, huone_id):

        json_data = request.get_json()

        data, errors = huoneet_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Room not found'}, HTTPStatus.FORBIDDEN

        huone = Huoneet.get_by_id(huone_id=huone_id)

        if huone is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        huone.name = data.get('name') or huone.name

        huone.save()

        return huoneet_schema.dump(huone).data, HTTPStatus.OK
