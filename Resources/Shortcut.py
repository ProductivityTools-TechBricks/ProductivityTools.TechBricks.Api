from flask import request,jsonify
from flask_restful import Resource
from http import HTTPStatus
from extensions import firestoredb

class ShortcutResource(Resource):
    def get(self):
        shortucts=firestoredb.collection('shortcuts').stream()
        my_dict = {el.id: el.to_dict() for el in shortucts}
        result=[]
        shortucts2=firestoredb.collection('shortcuts').stream()
        for doc in shortucts2:
            result.append(doc.to_dict())
        return result, HTTPStatus.OK

    def post(self):
        shortcuts=firestoredb.collection('shortcuts')
        shortcuts.document().set(request.json)
