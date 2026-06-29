from flask import render_template
from flask_login import login_required
from sqlalchemy import extract, func

from app.extensions import db
from app.models.attendance import Attendance
from app.reports import reports_bp

from flask import request
from datetime import datetime

# ===============================
# Reports Home
# ===============================
@reports_bp.route("/")
@login_required
def index():

    total = Attendance.query.count()

    present = Attendance.query.filter_by(status="Present").count()
    late = Attendance.query.filter_by(status="Late").count()
    absent = Attendance.query.filter_by(status="Absent").count()

    overall_percentage = round(
        ((present + late) / total) * 100, 2
    ) if total else 0

    return render_template(
        "reports/index.html",
        overall_percentage=overall_percentage,
        total_records=total,
        present=present,
        late=late,
        absent=absent
    )


# ===============================
# Monthly Report
# ===============================
@reports_bp.route("/monthly")
@login_required
def monthly():

    selected_month = request.args.get("month")

    query = Attendance.query

    if selected_month:
        year, month = selected_month.split("-")

        query = query.filter(
            extract("year", Attendance.date) == int(year),
            extract("month", Attendance.date) == int(month)
        )

    attendance = query.order_by(Attendance.date.desc()).all()

    total_records = len(attendance)

    present = sum(1 for a in attendance if a.status == "Present")
    late = sum(1 for a in attendance if a.status == "Late")
    absent = sum(1 for a in attendance if a.status == "Absent")

    attendance_percentage = round(
        ((present + late) / total_records) * 100,
        2
    ) if total_records else 0

    return render_template(
        "reports/monthly.html",
        attendance=attendance,
        total_records=total_records,
        present=present,
        late=late,
        absent=absent,
        attendance_percentage=attendance_percentage,
        selected_month=selected_month or ""
    )

# ===============================
# Yearly Report
# ===============================
@reports_bp.route("/yearly")
@login_required
def yearly():

    result = (
        db.session.query(
            extract("year", Attendance.date).label("year"),
            Attendance.status,
            func.count().label("count")
        )
        .group_by(
            extract("year", Attendance.date),
            Attendance.status
        )
        .order_by(
            extract("year", Attendance.date)
        )
        .all()
    )

    report = {}

    for year, status, count in result:

        year = int(year)

        if year not in report:
            report[year] = {
                "Present": 0,
                "Late": 0,
                "Absent": 0
            }

        report[year][status] = count

    labels = []
    totals = []
    percentages = []
    table = []

    overall_present = 0
    overall_late = 0
    overall_absent = 0

    for year in sorted(report.keys()):

        p = report[year]["Present"]
        l = report[year]["Late"]
        a = report[year]["Absent"]

        total = p + l + a

        percentage = round(
            ((p + l) / total) * 100,
            2
        ) if total else 0

        labels.append(str(year))
        totals.append(total)
        percentages.append(percentage)

        table.append({
            "year": year,
            "present": p,
            "late": l,
            "absent": a,
            "total": total,
            "percentage": percentage
        })

        overall_present += p
        overall_late += l
        overall_absent += a

    overall_total = overall_present + overall_late + overall_absent

    overall_percentage = round(
        ((overall_present + overall_late) / overall_total) * 100,
        2
    ) if overall_total else 0

    return render_template(
        "reports/yearly.html",
        labels=labels,
        totals=totals,
        percentages=percentages,
        table=table,
        overall_percentage=overall_percentage
    )