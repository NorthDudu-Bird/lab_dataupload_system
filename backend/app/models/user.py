from .base import TimestampMixin, format_value
from ..extensions import db


class SysUser(db.Model, TimestampMixin):
    __tablename__ = "sys_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="enabled")

    def to_dict(self, include_password=False):
        data = {
            "id": self.id,
            "username": self.username,
            "real_name": self.real_name,
            "phone": self.phone,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "create_time": format_value(self.create_time),
            "update_time": format_value(self.update_time),
        }
        if include_password:
            data["password"] = self.password
        return data

