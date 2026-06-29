from datetime import date

from app.extensions import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    employee_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    gender = db.Column(
        db.String(20)
    )

    date_of_birth = db.Column(
        db.Date
    )

    joining_date = db.Column(
        db.Date,
        default=date.today
    )

    designation = db.Column(
        db.String(100),
        nullable=False
    )

    salary = db.Column(
        db.Float,
        default=0
    )

    address = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    shift = db.Column(
        db.String(50),
        default="General Shift (09:00–18:00)"
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship(
        "Department",
        back_populates="employees"
    )

    attendance = db.relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete-orphan",
        lazy=True
    )

    leave_requests = db.relationship(
    "Leave",
    back_populates="employee",
    cascade="all, delete-orphan",
    lazy=True
    )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Employee {self.employee_code}>"