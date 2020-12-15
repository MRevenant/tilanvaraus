from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.varaus import Varaus
from extensions import db
from schemas.varaus import VarausSchema

varaus_schema = VarausSchema()
varaus_list_schema = VarausSchema(many=True)


class VarausListResource(Resource):

    def get(self):

        varaukset = Varaus.get_all_published()

        return varaus_list_schema.dump(varaukset).data, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = varaus_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        varaus = Varaus(**data)
        varaus.user_id = current_user
        varaus.save()

        return varaus_schema.dump(varaus).data, HTTPStatus.CREATED

    @jwt_required
    def patch(self, varaus_id):

        json_data = request.get_json

        data, errors = varaus_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        varaus = Varaus.get_by_id(varaus_id=varaus_id)

        if varaus in None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != varaus.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        varaus.tila = data.get('tila') or varaus.tila
        varaus.paiva = data.get('paiva') or varaus.paiva
        varaus.aika = data.get('aika') or varaus.aika
        varaus.henkiloita = data.get('henkiloita') or varaus.henkiloita
        varaus.kuka = data.get('kuka') or varaus.kuka
        varaus.sahkoposti = data.get('sahkoposti') or varaus.sahkoposti

        varaus.save()

        return varaus_schema.dump(varaus).data, HTTPStatus.OK


class VarausResource(Resource):

    @jwt_optional
    def get(self, varaus_id):

        varaus = Varaus.get_by_id(varaus_id=varaus_id)

        if varaus is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if varaus.is_publish == False and varaus.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return varaus.data(), HTTPStatus.OK

    @jwt_required
    def put(self, varaus_id):

        json_data = request.get_json()

        varaus = Varaus.get_by_id(varaus_id=varaus_id)

        if varaus is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != varaus.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        varaus.tila = json_data['tila']
        varaus.paiva = json_data['paiva']
        varaus.aika = json_data['aika']
        varaus.henkiloita = json_data['henkiloita']
        varaus.kuka = json_data['kuka']
        varaus.sahkoposti = json_data['sahkopösti']

        varaus.save()

        return varaus.data, HTTPStatus.OK

    @jwt_required
    def delete(self, varaus_id):
        varaus = Varaus.get_by_id(varaus_id=varaus_id)

        if varaus is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != varaus.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        varaus.is_publish = False
        varaus.delete(self)

        return {}, HTTPStatus.NO_CONTENT


class VarausPublishResource(Resource):

    def put(self, varaus_id):
        varaus = Varaus.get_by_id(varaus_id=varaus_id)

        if varaus is None:
            return{'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != varaus.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        varaus.is_publish = True
        varaus.save()

        return{}, HTTPStatus.CREATED

    @jwt_required
    def delete(self, varaus_id):
        varaus = Varaus.get_by_id(varaus_id=varaus_id)

        if varaus is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != varaus.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        varaus.is_publish = False
        varaus.delete()

        return {}, HTTPStatus.NO_CONTENT
