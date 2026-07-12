from flask import Flask
from flask_cors import CORS

from app.extensions import db, jwt


def create_app():

    app = Flask(__name__)


    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///niyukt.db"

    app.config["JWT_SECRET_KEY"] = ("IronMAN")

    # Vue frontend communication for api
    CORS(
            app,
            origins=[
                "http://localhost:8080"
                ]
            )


    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False


    db.init_app(app)
    jwt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(
        user_bp,
        url_prefix="/api"
    )
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )


    with app.app_context():
        db.create_all()


    return app
