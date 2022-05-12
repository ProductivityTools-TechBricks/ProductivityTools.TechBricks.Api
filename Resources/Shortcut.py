from flask import request,jsonify
from flask_restful import Resource
from http import HTTPStatus
from extensions import firestoredb

class ShortcutResource(Resource):
    def get(self):
        shortucts=firestoredb.collection('shortcuts').stream()
        my_dict = {el.id: el.to_dict() for el in shortucts}
        return my_dict, HTTPStatus.OK

    def post(self):
        shortcuts=firestoredb.collection('shortcuts')
        shortcuts.document().set(request.json)
