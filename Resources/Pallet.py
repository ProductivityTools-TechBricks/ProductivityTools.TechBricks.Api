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

    def decode_token(self):
        """Returns the decoded Firebase ID token or None if missing/invalid/expired.

        ID tokens live for 1 hour; the web client refreshes them from the
        long-lived Firebase session and retries once on 401, so invalid tokens
        must result in 401 (not 500).
        """
        id_token = request.headers.get('Authorization', '')
        id_token = id_token.replace("Bearer", "")
        id_token = id_token.replace(" ", "")
        if id_token in ('', 'null', 'undefined'):
            return None
        try:
            return auth.verify_id_token(id_token)
        except (auth.ExpiredIdTokenError, auth.RevokedIdTokenError, auth.InvalidIdTokenError) as e:
            print("Token validation failed:", e)
            return None
        except ValueError as e:
            print("Token validation failed:", e)
            return None

    def get_user_name(self):
        """Returns the caller's user name (gmail login) or None if not authenticated.

        Owners of a pallet are stored as gmail logins (email without
        '@gmail.com'), so the caller is identified the same way. Only verified
        emails are accepted, otherwise anybody could register an account with
        somebody else's address.
        """
        decoded_token = self.decode_token()
        if decoded_token is None:
            return None
        token_email = decoded_token.get("email")
        if not token_email or not decoded_token.get("email_verified", False):
            return None
        return token_email.replace("@gmail.com", "")

    def get_owned_pallet(self, pallet_id, user_name):
        """Loads a pallet and checks that user_name is one of its owners.

        Returns (document_reference, pallet_dict, None) on success or
        (None, None, error_response) when the pallet is missing or not owned.
        """
        if not pallet_id:
            return None, None, ({'message': 'document_id is required'}, HTTPStatus.BAD_REQUEST)
        pallet = firestoredb.collection('pallet').document(pallet_id)
        doc = pallet.get()
        if not doc.exists:
            return None, None, ({'message': 'pallet not found'}, HTTPStatus.NOT_FOUND)
        pallet_dict = doc.to_dict()
        if user_name not in pallet_dict.get("owners", []):
            return None, None, ({'message': 'you are not an owner of this pallet'}, HTTPStatus.FORBIDDEN)
        return pallet, pallet_dict, None

    UNAUTHORIZED_RESPONSE = ({'message': 'access token is incorrect'}, HTTPStatus.UNAUTHORIZED)

    @expects_json(addSchema)
    def put(self):
        user_name = self.get_user_name()
        if user_name is None:
            return self.UNAUTHORIZED_RESPONSE
        pallet = dict(request.json)
        owners = list(pallet.get("owners") or [])
        # The creator always owns the pallet they create.
        if user_name not in owners:
            owners.append(user_name)
        pallet["owners"] = owners
        pallet.setdefault("bricks", [])
        palette = firestoredb.collection('pallet')
        palette.document().set(pallet)
        return {'message': 'created'}, HTTPStatus.OK

    def post(self):
        user_name = self.get_user_name()
        if user_name is None:
            return self.UNAUTHORIZED_RESPONSE

        document_id = request.json.get("document_id")
        pallet, _, error = self.get_owned_pallet(document_id, user_name)
        if error:
            return error
        updated = dict(request.json)
        owners = updated.get("owners")
        # An owner must not be able to accidentally remove themselves
        # (or everybody) and lose access to the pallet.
        if not isinstance(owners, list) or user_name not in owners:
            return {'message': 'owners must be a list containing the current user'}, HTTPStatus.BAD_REQUEST
        pallet.set(updated)
        return {'message': 'updated'}, HTTPStatus.OK

    def get(self):
        user_name = self.get_user_name()
        if user_name is None:
            return self.UNAUTHORIZED_RESPONSE

        owner = request.args.get('owner') or user_name
        result = []

        pallets = firestoredb.collection('pallet').where(filter=FieldFilter("owners", 'array_contains', owner)).stream()
        for doc in pallets:
            partResult = doc.to_dict()
            # Only pallets the caller co-owns are visible. Looking at another
            # user's page shows just the pallets shared with the caller.
            if user_name not in partResult.get("owners", []):
                continue
            partResult["document_id"] = doc.id
            result.append(partResult)

        return result, HTTPStatus.OK

    def delete(self):
        user_name = self.get_user_name()
        if user_name is None:
            return self.UNAUTHORIZED_RESPONSE
        pallet, _, error = self.get_owned_pallet(request.json.get('document_id'), user_name)
        if error:
            return error
        print("remove")
        pallet.delete()
        return {'message': 'deleted'}, HTTPStatus.OK

    def patch(self):
        user_name = self.get_user_name()
        if user_name is None:
            return self.UNAUTHORIZED_RESPONSE

        name = request.json.get('name')
        if not isinstance(name, str) or not name:
            return {'message': 'name is required'}, HTTPStatus.BAD_REQUEST
        pallet, _, error = self.get_owned_pallet(request.json.get('document_id'), user_name)
        if error:
            return error
        print("rename")
        pallet.update({"name": name})
        return {'message': 'renamed'}, HTTPStatus.OK
