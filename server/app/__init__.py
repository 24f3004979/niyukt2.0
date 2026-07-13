from flask import Flask
from flask_cors import CORS

from app.extensions import db, jwt

from app.models.user import User
from app.models.drive import Drive
from app.models.application import Application
from app.models.placement_history import PlacementHistory

__all__ = ["User", "Drive", "Application", "PlacementHistory"]


def create_app():

    app = Flask(__name__)


    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///niyukt.db"

    app.config["JWT_SECRET_KEY"] = ("lqppgc9qr_clash_of_clans_id_freefire_india_instant_damage_skill")

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
    from app.routes.admin_routes import admin_bp
    from app.routes.company_routes import company_bp
    from app.routes.student_routes import student_bp

    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/admin"
    )
    app.register_blueprint(
        user_bp,
        url_prefix="/api/user"
    )
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    with app.app_context():
        db.create_all()


    return app
