from flask import request
from flask_restful import Resource
from flask_expects_json import expects_json
from http import HTTPStatus
from extensions import firestoredb
from firebase_admin import auth
from google.cloud.firestore_v1.base_query import FieldFilter


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

    def validate_token(self):
        id_token = request.headers.environ['HTTP_AUTHORIZATION']
        id_token = id_token.replace("Bearer", "")
        id_token = id_token.replace(" ", "")
        if id_token == 'null':
            return False
        decoded_token = auth.verify_id_token(id_token)
        print(decoded_token)
        
    def validate_user_with_token(self,user_names):
        id_token = request.headers.environ['HTTP_AUTHORIZATION']
        id_token = id_token.replace("Bearer", "")
        id_token = id_token.replace(" ", "")
        if id_token == 'null':
            return False
        decoded_token = auth.verify_id_token(id_token)
        token_email=decoded_token["email"]
        tokan_name=token_email.replace("@gmail.com","")
        if tokan_name in user_names:
            return True
        return False
        print(decoded_token)

    @expects_json(addSchema)
    def put(self):
        if self.validate_token() == False:
            return {'message': 'access token is incorrect'}, HTTPStatus.UNAUTHORIZED
        palette = firestoredb.collection('pallet')
        palette.document().set(request.json)

    def post(self):
        if self.validate_token()==False:
            return {'message': 'access token is incorrect'}, HTTPStatus.UNAUTHORIZED

        document_id=request.json["document_id"]
        firestoredb.collection('pallet').document(document_id).set(request.json)

    def get(self):
        owner=request.args['owner']
        #owner = "pwujczyk@gmail.com"
        result=[]


        pallets=firestoredb.collection('pallet').where(filter=FieldFilter("owners",'array_contains',owner)).stream()
        for doc in pallets:
            partResult=doc.to_dict();
            partResult["document_id"]=doc.id
            result.append(partResult)

        return result,HTTPStatus.OK
    
    def delete(self):
        
        x= self.validate_token()
        palletId=request.json['document_id'];
        pellet=firestoredb.collection('pallet').document(palletId)
        doc=pellet.get();
        pellet_dict=doc.to_dict();
        user_names=pellet_dict["owners"]
        if self.validate_user_with_token(user_names):
            print("remove")
            pellet.delete()
            return HTTPStatus.OK
        else:
            return HTTPStatus.UNAUTHORIZED
        
        