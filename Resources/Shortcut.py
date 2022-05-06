from flask import request
from flask_restful import Resource
from http import HTTPStatus

class ShortcutResource(Resource):
    def get(self):
        return {'data':'pawel12'}, HTTPStatus.OK