from flask import request, jsonify
from flask_expects_json import expects_json
from flask_restful import Resource
from http import HTTPStatus
from extensions import firestoredb
from firebase_admin import auth


class ShortcutResource(Resource):
    def get(self):
        id_token = request.headers.environ['HTTP_AUTHORIZATION']
        id_token = id_token.replace("Bearer", "")
        id_token = id_token.replace(" ", "")

        # xx=auth.verify_id_token()
        decoded_token = auth.verify_id_token(id_token)

        shortucts = firestoredb.collection('shortcuts').stream()
        my_dict = {el.id: el.to_dict() for el in shortucts}
        result = []
        shortucts2 = firestoredb.collection('shortcuts').stream()
        for doc in shortucts2:
            partResult = doc.to_dict()
            partResult["document_id"] = doc.id
            result.append(partResult)
        return result, HTTPStatus.OK

    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string"
                        },
                        "value": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }

    @expects_json(schema)
    def post(self):
        shortcuts = firestoredb.collection('shortcuts')
        shortcuts.document().set(request.json)
