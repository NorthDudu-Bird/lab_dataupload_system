from .base import TimestampMixin, format_value
from ..extensions import db


class SysNotice(db.Model, TimestampMixin):
    __tablename__ = "sys_notice"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey("sys_user.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="published")
    published_time = db.Column(db.DateTime)

    publisher = db.relationship("SysUser")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "publisher_id": self.publisher_id,
            "publisher_name": self.publisher.real_name if self.publisher else None,
            "status": self.status,
            "published_time": format_value(self.published_time),
            "create_time": format_value(self.create_time),
            "update_time": format_value(self.update_time),
        }

