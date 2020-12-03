from flask import Flask
from . import main, shoe


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.register_blueprint(main.home)
    app.register_blueprint(shoe.shoe)
    return app
