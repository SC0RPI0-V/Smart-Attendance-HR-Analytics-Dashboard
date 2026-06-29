from datetime import date

from app.extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    date = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Present",
        nullable=False
    )

    check_in = db.Column(db.Time)

    check_out = db.Column(db.Time)

    employee = db.relationship(
        "Employee",
        back_populates="attendance"
    )

    def __repr__(self):
        return f"<Attendance {self.employee_id} - {self.date}>"