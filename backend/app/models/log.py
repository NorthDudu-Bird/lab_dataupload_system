from .base import TimestampMixin, format_value
from ..extensions import db


class OperationLog(db.Model, TimestampMixin):
    __tablename__ = "operation_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("sys_user.id"))
    module = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500))
    ip_address = db.Column(db.String(50))

    user = db.relationship("SysUser")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.user.username if self.user else None,
            "module": self.module,
            "action": self.action,
            "content": self.content,
            "ip_address": self.ip_address,
            "create_time": format_value(self.create_time),
            "update_time": format_value(self.update_time),
        }

