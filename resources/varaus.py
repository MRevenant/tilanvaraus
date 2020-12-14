from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.varaus import Varaus, varaus_list


class VarausListResource(Resource):

    def get(self):
        data = []
        for varaus in varaus_list:
            if varaus.is_publish is True:
                data.append(varaus.data)
        return{'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        varaus = Varaus(tila=data["tila"],
                        paiva=data["paiva"],
                        aika=data["aika"],
                        henkiloita=data["henkiloita"],
                        kuka=data["kuka"],
                        sahkoposti=data["sahkoposti"])
        varaus_list.append(varaus)
        return varaus.data, HTTPStatus.CREATED


class VarausResource(Resource):

    def get(self, varaus_id):
        varaus = next((varaus for varaus in varaus_list if varaus.id == varaus_id and varaus.is_publish == True),
                      None)

        if varaus is None:
            return{'message': 'Varaus not found'}, HTTPStatus.NOT_FOUND

        return varaus.data, HTTPStatus.OK

    def put(self, varaus_id):
        data = request.get_json()

        varaus = next((varaus for varaus in varaus_list if varaus.id == varaus_id), None)

        if varaus is None:
            return{'message': 'Varaus not found'}, HTTPStatus.NOT_FOUND

        varaus.tila = data['tila']
        varaus.paiva = data['päivä']
        varaus.aika = data['aika']
        varaus.henkiloita = data['henkilöitä']
        varaus.kuka = data['kuka']
        varaus.sahkoposti = data['sahkopösti']

        return varaus.data, HTTPStatus.OK


class VarausPublishResource(Resource):

    def put(self, varaus_id):
        varaus = next((varaus for varaus in varaus_list if varaus.id == varaus_id), None)

        if varaus is None:
            return{'message': 'Varaus not found'}, HTTPStatus.NOT_FOUND

        varaus.is_publish = True

        return(), HTTPStatus.CREATED

    def delete(self, varaus_id):
        varaus = next((varaus for varaus in varaus_list if varaus.id == varaus_id), None)

        if varaus is None:
            return {'message': 'Varaus not found'}, HTTPStatus.NOT_FOUND

        varaus.is_publish = False

        return (), HTTPStatus.NO_CONTENT