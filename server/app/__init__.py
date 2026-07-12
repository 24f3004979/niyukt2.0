from flask import Flask

from app.extensions import db


def create_app():

    app = Flask(__name__)


    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///niyukt.db"


    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False


    db.init_app(app)


    from app.routes.user_routes import user_bp

    app.register_blueprint(
        user_bp,
        url_prefix="/api"
    )


    with app.app_context():
        db.create_all()


    return app
