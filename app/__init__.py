from flask import Flask
import os

from app.extensions import db
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)

    # -----------------------------
    # CONFIG
    # -----------------------------
    app.config["SECRET_KEY"] = "secret-key"

    # IMPORTANT FIX: force instance database path
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, "hr.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # -----------------------------
    # EXTENSIONS
    # -----------------------------
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # -----------------------------
    # BLUEPRINTS
    # -----------------------------
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.employees.routes import employees_bp
    from app.departments.routes import departments_bp
    from app.attendance.routes import attendance_bp
    from app.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employees_bp, url_prefix="/employees")
    app.register_blueprint(departments_bp, url_prefix="/departments")
    app.register_blueprint(attendance_bp, url_prefix="/attendance")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    # -----------------------------
    # DB INIT
    # -----------------------------
    with app.app_context():
        db.create_all()

    return app