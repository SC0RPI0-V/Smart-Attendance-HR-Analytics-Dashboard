from app.extensions import db


class Holiday(db.Model):
    __tablename__ = "holidays"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    holiday_name = db.Column(
        db.String(100),
        nullable=False
    )

    holiday_date = db.Column(
        db.Date,
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.Text
    )

    def __repr__(self):
        return f"<Holiday {self.holiday_name}>"