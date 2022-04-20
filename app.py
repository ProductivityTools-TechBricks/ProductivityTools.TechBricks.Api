from flask import Flask
from flask_restful import Api

from Resources.CardResource import CardResource

def create_app():
    app=Flask(__name__)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    x=1

def register_resources(app):
    api=Api(app)
    api.add_resource(CardResource, '/Card')

if __name__=="__main__":
    app=create_app()
    app.run(port=5000,debug=True)