from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from app.extensions import db
from app.models.employee import Employee
from app.models.department import Department
from app.models.attendance import Attendance
from app.models.leave import Leave
from app.models.holiday import Holiday


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard",
    template_folder="../templates"
)


@dashboard_bp.route("/")
@login_required
def dashboard():

    today = date.today()

    # =========================
    # BASIC COUNTS
    # =========================
    total_employees = Employee.query.count()
    total_departments = Department.query.count()

    active_employees = Employee.query.filter_by(status="Active").count()
    inactive_employees = Employee.query.filter_by(status="Inactive").count()

    total_leave = Leave.query.count()
    total_holidays = Holiday.query.count()

    # =========================
    # TODAY ATTENDANCE (FIXED + SAFE)
    # =========================
    today_attendance = Attendance.query.filter(
        Attendance.date == today
    ).all()

    # fallback if no data for today
    if not today_attendance:
        latest_date = db.session.query(func.max(Attendance.date)).scalar()

        if latest_date:
            today_attendance = Attendance.query.filter(
                Attendance.date == latest_date
            ).all()

    present_today = sum(1 for a in today_attendance if a.status == "Present")
    absent_today = sum(1 for a in today_attendance if a.status == "Absent")

    # =========================
    # RECENT ATTENDANCE
    # =========================
    recent_attendance = (
        Attendance.query
        .order_by(Attendance.date.desc())
        .limit(10)
        .all()
    )

    # =========================
    # DEPARTMENT SUMMARY (FIXED JOIN)
    # =========================
    department_summary = db.session.query(
        Department.department_name,
        func.count(Employee.id)
    ).join(Employee, Employee.department_id == Department.id) \
     .group_by(Department.id) \
     .all()

    # =========================
    # RECENT EMPLOYEES
    # =========================
    recent_employees = (
        Employee.query
        .order_by(Employee.id.desc())
        .limit(5)
        .all()
    )

    # =========================
    # RENDER TEMPLATE
    # =========================
    return render_template(
        "dashboard/index.html",

        # counts
        total_employees=total_employees,
        total_departments=total_departments,
        active_employees=active_employees,
        inactive_employees=inactive_employees,

        # attendance overview
        present_today=present_today,
        absent_today=absent_today,
        today_attendance=today_attendance,

        # extras
        total_leave=total_leave,
        total_holidays=total_holidays,
        recent_attendance=recent_attendance,
        recent_employees=recent_employees,

        # charts
        department_summary=department_summary,

        # context
        today=today,
        current_user=current_user
    )