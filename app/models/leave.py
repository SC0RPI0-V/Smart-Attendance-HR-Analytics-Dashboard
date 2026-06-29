from datetime import date

from app.extensions import db


class Leave(db.Model):
    __tablename__ = "leave_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    leave_type = db.Column(
        db.String(50),
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    reason = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    applied_on = db.Column(
        db.Date,
        default=date.today
    )

    employee = db.relationship(
        "Employee"
    )

    def __repr__(self):
        return f"<Leave {self.id}>"