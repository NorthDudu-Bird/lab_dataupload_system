from flask import Flask

from .common.exceptions import register_error_handlers
from .config import Config
from .extensions import cors, db, jwt
from .models import *  # noqa: F401,F403
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .routes.equipments import equipments_bp
from .routes.labs import labs_bp
from .routes.notices import notices_bp
from .routes.reports import reports_bp
from .routes.reviews import reviews_bp
from .routes.users import users_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.ensure_ascii = False

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    register_error_handlers(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(labs_bp, url_prefix="/api/labs")
    app.register_blueprint(equipments_bp, url_prefix="/api/equipments")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(reviews_bp, url_prefix="/api/reviews")
    app.register_blueprint(notices_bp, url_prefix="/api/notices")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    return app
