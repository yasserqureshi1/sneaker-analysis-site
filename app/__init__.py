from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    from . import views
    app.register_blueprint(views.view)

    return app
