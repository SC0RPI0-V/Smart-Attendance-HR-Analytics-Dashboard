from flask import Blueprint, render_template
from flask_login import login_required

from app.models.department import Department

departments_bp = Blueprint(
    "departments",
    __name__,
    url_prefix="/departments",
    template_folder="../templates"
)


@departments_bp.route("/")
@login_required
def index():

    departments = (
        Department.query
        .order_by(Department.department_name.asc())
        .all()
    )

    print("=" * 50)
    print("Departments Loaded:", len(departments))

    for dept in departments:
        print(
            dept.id,
            dept.department_name,
            dept.department_code
        )

    print("=" * 50)

    return render_template(
        "departments/index.html",
        departments=departments
    )