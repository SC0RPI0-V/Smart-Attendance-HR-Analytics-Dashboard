from app.extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    department_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    department_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    description = db.Column(db.Text)

    employees = db.relationship(
        "Employee",
        back_populates="department",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Department {self.department_name}>"