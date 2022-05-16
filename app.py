from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors  import CORS
from extensions import db
import os
from config import Config

from Resources.Shortcut import ShortcutResource

def create_app():
    app=Flask(__name__)
    #CORS(app)
    app.config.from_object(Config)

    #register_extensions(app)
    register_resources(app)

    return app

#def register_extensions(app):
#    db.init_app(app)
#    migrate=Migrate(app,db)

def register_resources(app):
    api=Api(app)
    api.add_resource(ShortcutResource, '/Card')

if __name__=="__main__":
    app=create_app()
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)