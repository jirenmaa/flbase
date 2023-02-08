from flask import Flask

from firebase_admin import credentials, initialize_app

# firebase > project settings > generate new private key
cred = credentials.Certificate("key.json")
initialize_app(cred)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'FyQ8]R=o^fbyx<xRUKyd?AcLS;@u@o'

    from .service import service

    app.register_blueprint(service, url_prefix="/api")

    return app
