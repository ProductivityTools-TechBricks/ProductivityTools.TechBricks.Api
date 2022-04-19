from flask import Flask

def create_app():
    app=Flask(__name__)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    x=1

def register_resources(app):
    y=2

if __name__=="__main__":
    app=create_app()
    app.run(port=5000,debug=True)