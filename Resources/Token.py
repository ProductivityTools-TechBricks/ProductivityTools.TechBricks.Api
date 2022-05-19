from flask import request,jsonify, Response
from flask_restful import Resource
from http import HTTPStatus
from extensions import firestoredb
from firebase_admin import auth

class TokenResource(Resource):
    def get(self):

        custom_token=auth.create_custom_token("pawel123");
        return Response(custom_token, mimetype="text/plain", direct_passthrough=True)


