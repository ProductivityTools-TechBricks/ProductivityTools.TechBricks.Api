from firebase_admin import credentials, firestore, initialize_app
from flask_jwt_extended import JWTManager
# from flask_sqlalchemy import SQLAlchemy
#
#
# db=SQLAlchemy()

cred=credentials.Certificate('pttechbricksapi-firebase.json')
default_app=initialize_app(cred)
firestoredb=firestore.client()

jwt=JWTManager()