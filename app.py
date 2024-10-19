from flask import Flask
from flask_restful import Api
#from flask_migrate import Migrate
from flask_cors  import CORS
import os
from config import Config

from Resources.Date import DateResource
from Resources.Pallet import PalletResource
from Resources.Shortcut import ShortcutResource
from Resources.Token import TokenResource
from Resources.Brick import BrickResource

def create_app():
    app=Flask(__name__)
    CORS(app)
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
    api.add_resource(TokenResource, '/Token')
    api.add_resource(BrickResource,'/Brick')
    api.add_resource(PalletResource,'/pallet')
    api.add_resource(DateResource,'/Date')

if __name__=="__main__":
    app=create_app()
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)