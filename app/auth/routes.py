from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates"
)


# ----------------------------
# Login
# ----------------------------

@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(
                user,
                remember=remember
            )

            flash(
                f"Welcome back, {user.username}!",
                "success"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "auth/login.html"
    )


# ----------------------------
# Register
# ----------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing:

            flash(
                "Email already exists.",
                "warning"
            )

            return redirect(
                url_for("auth.register")
            )

        user = User(

            username=username,

            email=email,

            role=role

        )

        user.password_hash = generate_password_hash(
            password
        )

        db.session.add(user)

        db.session.commit()

        flash(
            "User created successfully.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html"
    )


# ----------------------------
# Logout
# ----------------------------

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )