from flask import request
from flask_restful import Resource
from http import HTTPStatus
from extensions import firestoredb

class ShortcutResource(Resource):
    def get(self):
        return {'data':'pawel12'}, HTTPStatus.OK

    def post(self):
        shortcuts=firestoredb.collection('shortcuts')
        shortcuts.document().set(request.json)
