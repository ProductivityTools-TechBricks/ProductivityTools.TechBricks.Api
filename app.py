from flask import Flask
from flask_restful import Api
import os

from Resources.Shortcut import ShortcutResource

def create_app():
    app=Flask(__name__)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    x=1

def register_resources(app):
    api=Api(app)
    api.add_resource(ShortcutResource, '/Card')

if __name__=="__main__":
    app=create_app()
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)