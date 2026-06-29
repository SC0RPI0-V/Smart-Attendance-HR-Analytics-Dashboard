from datetime import date, datetime
import io

from flask import make_response, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.attendance import attendance_bp
from app.extensions import db
from app.models.employee import Employee
from app.models.attendance import Attendance
from sqlalchemy import extract
import csv
from io import StringIO
from flask import Response

# ============================
# Attendance Home / History
# ============================

@attendance_bp.route("/")
@login_required
def index():

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    attendance_date = request.args.get("date", "")

    query = Attendance.query

    if search:
        query = query.join(Employee).filter(
            (Employee.first_name.ilike(f"%{search}%")) |
            (Employee.last_name.ilike(f"%{search}%")) |
            (Employee.employee_code.ilike(f"%{search}%"))
        )

    if status:
        query = query.filter(Attendance.status == status)

    if attendance_date:
        query = query.filter(Attendance.date == attendance_date)

    attendance = (
        query.order_by(Attendance.date.desc())
        .all()
    )

    return render_template(
        "attendance/index.html",
        attendance=attendance,
        search=search,
        status=status,
        attendance_date=attendance_date
    )
# ============================
# Mark Attendance
# ============================
@attendance_bp.route("/mark", methods=["GET", "POST"])
@login_required
def mark_attendance():

    employees = Employee.query.order_by(Employee.first_name).all()

    if request.method == "POST":

        attendance_date= datetime.strptime(
            request.form["attendance_date"],
            "%Y-%m-%d"
        ).date()

        for emp in employees:

            status = request.form.get(f"status_{emp.id}")

            record = Attendance.query.filter_by(
                employee_id=emp.id,
                date=attendance_date
            ).first()

            if record:
                record.status = status
            else:
                db.session.add(
                    Attendance(
                        employee_id=emp.id,
                        date=attendance_date,
                        status=status
                    )
                )

        db.session.commit()

        flash(
            "Attendance marked successfully!",
            "success"
        )

        return redirect(url_for("attendance.index"))

    return render_template(
        "attendance/mark.html",
        employees=employees,
        today=date.today().isoformat()
    )

# ------------------------------------
# DELETE ATTENDANCE
# ------------------------------------
@attendance_bp.route("/delete/<int:id>")
@login_required
def delete_attendance(id):

    attendance = Attendance.query.get_or_404(id)

    db.session.delete(attendance)
    db.session.commit()

    flash("Attendance record deleted successfully.", "success")

    return redirect(url_for("attendance.index"))





@attendance_bp.route("/monthly")
@login_required
def monthly_report():

    month = request.args.get("month", type=int)

    year = request.args.get("year", type=int)

    today = date.today()

    if not month:
        month = today.month

    if not year:
        year = today.year

    employees = Employee.query.order_by(Employee.first_name).all()

    report = []

    for emp in employees:

        records = Attendance.query.filter(
            Attendance.employee_id == emp.id,
            extract("month", Attendance.date) == month,
            extract("year", Attendance.date) == year
        ).all()

        present = sum(1 for r in records if r.status == "Present")
        absent = sum(1 for r in records if r.status == "Absent")
        late = sum(1 for r in records if r.status == "Late")

        total = len(records)

        percentage = round((present + late) / total * 100, 2) if total else 0

        report.append({
            "employee": emp,
            "present": present,
            "absent": absent,
            "late": late,
            "total": total,
            "percentage": percentage
        })

    return render_template(
        "attendance/monthly.html",
        report=report,
        month=month,
        year=year
    )

@attendance_bp.route("/export")
@login_required
def export_csv():

    attendance = (
        Attendance.query
        .order_by(Attendance.date.desc())
        .all()
    )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Employee Code",
        "Employee Name",
        "Date",
        "Status"
    ])

    for record in attendance:

        writer.writerow([
            record.employee.employee_code,
            f"{record.employee.first_name} {record.employee.last_name}",
            record.date,
            record.status
        ])

    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = \
        "attachment; filename=attendance_report.csv"

    response.headers["Content-type"] = "text/csv"

    return response