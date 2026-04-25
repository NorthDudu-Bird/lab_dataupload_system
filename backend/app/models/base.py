from datetime import date, datetime

from ..extensions import db


def format_value(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return value


class TimestampMixin:
    create_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

