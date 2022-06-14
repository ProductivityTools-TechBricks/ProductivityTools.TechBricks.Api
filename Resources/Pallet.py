from flask import request
from flask_restful import Resource
from flask_expects_json import expects_json
from http import HTTPStatus
from extensions import firestoredb
from firebase_admin import auth

class PalletResource(Resource):

    addSchema={
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
    updateSchema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "owners": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "bricks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string"
                        },
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

    @expects_json(addSchema)
    def put(self):
        palette = firestoredb.collection('pallet')
        palette.document().set(request.json)

    def post(self):
        id_token = request.headers.environ['HTTP_AUTHORIZATION']
        id_token = id_token.replace("Bearer", "")
        id_token = id_token.replace(" ", "")
        if id_token == 'null':
            return {'message':'access token is incorrect'},HTTPStatus.UNAUTHORIZED
        decoded_token = auth.verify_id_token(id_token)


        document_id=request.json["document_id"]
        firestoredb.collection('pallet').document(document_id).set(request.json)

    def get(self):
        owner=request.args['owner']
        #owner = "pwujczyk@gmail.com"
        result=[]
        pallets=firestoredb.collection('pallet').where("owners",u'array_contains',owner).stream();
        for doc in pallets:
            partResult=doc.to_dict();
            partResult["document_id"]=doc.id
            result.append(partResult)
        return result,HTTPStatus.OK