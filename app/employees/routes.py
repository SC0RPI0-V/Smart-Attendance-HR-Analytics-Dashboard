from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from app.employees import employees_bp
from app.extensions import db
from app.models.employee import Employee
from app.models.department import Department


# =====================================
# EMPLOYEE LIST
# =====================================
@employees_bp.route("/")
@login_required
def index():

    search = request.args.get("search", "")

    query = Employee.query

    if search:

        query = query.filter(
            Employee.first_name.contains(search) |
            Employee.last_name.contains(search) |
            Employee.employee_code.contains(search) |
            Employee.email.contains(search)
        )

    employees = query.all()

    return render_template(
        "employees/list.html",
        employees=employees,
        search=search
    )


# =====================================
# VIEW EMPLOYEE
# =====================================
@employees_bp.route("/view/<int:id>")
@login_required
def view_employee(id):

    employee = Employee.query.get_or_404(id)

    return render_template(
        "employees/view.html",
        employee=employee
    )


# =====================================
# ADD EMPLOYEE
# =====================================
@employees_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_employee():

    departments = Department.query.all()

    if request.method == "POST":

        employee = Employee(

            employee_code=request.form["employee_code"],

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            email=request.form["email"],

            phone=request.form["phone"],

            gender=request.form["gender"],

            designation=request.form["designation"],

            joining_date=datetime.strptime(
                request.form["joining_date"],
                "%Y-%m-%d"
            ),

            salary=float(request.form["salary"]),

            status="Active",

            department_id=int(request.form["department_id"])

        )

        db.session.add(employee)
        db.session.commit()

        flash("Employee added successfully.", "success")

        return redirect(url_for("employees.index"))

    return render_template(
        "employees/add.html",
        departments=departments
    )


# =====================================
# EDIT EMPLOYEE
# =====================================
@employees_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_employee(id):

    employee = Employee.query.get_or_404(id)

    departments = Department.query.all()

    if request.method == "POST":

        employee.employee_code = request.form["employee_code"]
        employee.first_name = request.form["first_name"]
        employee.last_name = request.form["last_name"]
        employee.email = request.form["email"]
        employee.phone = request.form["phone"]
        employee.gender = request.form["gender"]
        employee.designation = request.form["designation"]
        employee.joining_date = datetime.strptime(
            request.form["joining_date"],
            "%Y-%m-%d"
        )
        employee.salary = float(request.form["salary"])
        employee.department_id = int(request.form["department_id"])

        db.session.commit()

        flash("Employee updated successfully.", "success")

        return redirect(url_for("employees.index"))

    return render_template(
        "employees/edit.html",
        employee=employee,
        departments=departments
    )


# =====================================
# DELETE EMPLOYEE
# =====================================
@employees_bp.route("/delete/<int:id>")
@login_required
def delete_employee(id):

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    flash("Employee deleted successfully.", "warning")

    return redirect(url_for("employees.index"))