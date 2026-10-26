from firebase_admin import credentials, firestore, initialize_app
# from flask_sqlalchemy import SQLAlchemy
#
#
# db=SQLAlchemy()

default_app=initialize_app()
firestoredb=firestore.client(database_id='techbricks')