from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

from app.extensions import db, jwt

from app.models.user import User
from app.models.drive import Drive
from app.models.application import Application
from app.models.placement_history import PlacementHistory

__all__ = ["User", "Drive", "Application", "PlacementHistory"]


def create_app():
    load_dotenv()

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
    app.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    app.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    # existing Flask-Mail config, if not already present:
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    from app.celery_app import  init_celery
    init_celery(app)

    print("BROKER URL:", app.config.get("CELERY_BROKER_URL"))

    # Register the two new blueprints alongside admin_bp
    from app.routes.admin_report_routes import admin_report_bp
    from app.routes.student_report_routes import student_report_bp

    app.register_blueprint(admin_report_bp)
    app.register_blueprint(student_report_bp)

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
