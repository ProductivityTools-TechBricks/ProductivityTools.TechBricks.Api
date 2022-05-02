from flask import request
from flask_restful import Resource
from http import HTTPStatus

class CardResource(Resource):
    def get(self):
        return {'data':'pawel1'}, HTTPStatus.OK