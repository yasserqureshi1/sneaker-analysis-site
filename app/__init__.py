from flask import Flask
from app.models import db
from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    db.init_app(app)

    from . import views
    app.register_blueprint(views.view)

    with app.app_context():
        db.create_all()
        db.session.commit()
    app.app_context().push()

    db.session.commit()

    return app
