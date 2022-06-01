from flask import request
from flask_restful import Resource
from flask_expects_json import expects_json

from extensions import firestoredb

class PalletResource(Resource):

    schema={
        "type":"object",
        "properties":{
            "name":{
                "type":"string"
            },
            "owners":{
                "type":"array",
                "items":{
                    "type":"string"
                }
            }
        }
    }

    @expects_json(schema)
    def post(self):
        palette = firestoredb.collection('pallet')
        palette.document().set(request.json)