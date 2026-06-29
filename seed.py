from datetime import date, timedelta
import random

from app import create_app
from app.extensions import db
from app.models import User, Department, Employee, Attendance

app = create_app()

with app.app_context():

    # =========================
    # CREATE TABLES
    # =========================
    db.create_all()

    # =========================
    # ADMIN USER
    # =========================
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@hrinsight.com",
            role="ADMIN"
        )
        admin.set_password("admin123")
        db.session.add(admin)

    # =========================
    # DEPARTMENTS
    # =========================
    departments = [
        ("HR", "Human Resources"),
        ("IT", "Information Technology"),
        ("FIN", "Finance")
    ]

    for code, name in departments:
        if not Department.query.filter_by(department_code=code).first():
            db.session.add(Department(
                department_code=code,
                department_name=name,
                description=f"{name} Department"
            ))

    db.session.commit()

    hr = Department.query.filter_by(department_code="HR").first()
    it = Department.query.filter_by(department_code="IT").first()
    fin = Department.query.filter_by(department_code="FIN").first()

    # =========================
    # EMPLOYEES
    # =========================
    employees_data = [
        ("EMP001","Rahul","Sharma","rahul@company.com","9876543201","Male","HR Manager",75000,hr),
        ("EMP002","Priya","Patel","priya@company.com","9876543202","Female","HR Executive",50000,hr),
        ("EMP003","Neha","Kapoor","neha@company.com","9876543203","Female","Recruiter",45000,hr),
        ("EMP004","Anjali","Joshi","anjali@company.com","9876543204","Female","Payroll Executive",48000,hr),
        ("EMP005","Karan","Malhotra","karan@company.com","9876543205","Male","HR Associate",40000,hr),
        ("EMP006","Arjun","Singh","arjun@company.com","9876543206","Male","Software Engineer",70000,it),
        ("EMP007","Sneha","Verma","sneha@company.com","9876543207","Female","Backend Developer",68000,it),
        ("EMP008","Rohan","Gupta","rohan@company.com","9876543208","Male","Frontend Developer",65000,it),
        ("EMP009","Pooja","Nair","pooja@company.com","9876543209","Female","DevOps Engineer",72000,it),
        ("EMP010","Aman","Mehta","aman@company.com","9876543210","Male","Cyber Security Analyst",80000,it),
        ("EMP011","Amit","Shah","amit@company.com","9876543211","Male","Finance Manager",85000,fin),
        ("EMP012","Simran","Kaur","simran@company.com","9876543212","Female","Accountant",55000,fin),
        ("EMP013","Vishal","Jain","vishal@company.com","9876543213","Male","Financial Analyst",60000,fin),
        ("EMP014","Deepika","Arora","deepika@company.com","9876543214","Female","Accounts Executive",50000,fin),
        ("EMP015","Mohit","Bansal","mohit@company.com","9876543215","Male","Auditor",58000,fin)
    ]

    for emp in employees_data:
        if not Employee.query.filter_by(employee_code=emp[0]).first():
            db.session.add(Employee(
                employee_code=emp[0],
                first_name=emp[1],
                last_name=emp[2],
                email=emp[3],
                phone=emp[4],
                gender=emp[5],
                designation=emp[6],
                salary=emp[7],
                joining_date=date(2025, 1, 1),
                status="Active",
                shift="General Shift (09:00–18:00)",
                department_id=emp[8].id
            ))

    db.session.commit()

    # =========================
    # ATTENDANCE (JAN 2025 → JUN 2026)
    # =========================
    employees = Employee.query.all()

    start_date = date(2025, 1, 1)
    end_date = date(2026, 6, 30)

    current = start_date
    records = []

    while current <= end_date:

        # skip weekends
        if current.weekday() < 5:

            for emp in employees:

                exists = Attendance.query.filter_by(
                    employee_id=emp.id,
                    date=current
                ).first()

                if not exists:

                    status = random.choices(
                        ["Present", "Late", "Absent"],
                        weights=[85, 5, 10],
                        k=1
                    )[0]

                    records.append(Attendance(
                        employee_id=emp.id,
                        date=current,
                        status=status
                    ))

        current += timedelta(days=1)

    db.session.bulk_save_objects(records)
    db.session.commit()

    print("=" * 50)
    print("✔ DATABASE SEEDED SUCCESSFULLY")
    print("Admin Email : admin@hrinsight.com")
    print("Password    : admin123")
    print("Employees   : 15")
    print("Attendance  : Jan 2025 → Jun 2026")
    print("=" * 50)