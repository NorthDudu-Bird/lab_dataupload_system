from .base import TimestampMixin, format_value
from ..extensions import db


class SysFile(db.Model, TimestampMixin):
    __tablename__ = "sys_file"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False, default=0)
    content_type = db.Column(db.String(100))
    uploader_id = db.Column(db.Integer, db.ForeignKey("sys_user.id"), nullable=False)
    related_report_id = db.Column(db.Integer, db.ForeignKey("lab_report.id"))

    uploader = db.relationship("SysUser")

    def to_dict(self):
        return {
            "id": self.id,
            "original_name": self.original_name,
            "stored_name": self.stored_name,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "uploader_id": self.uploader_id,
            "uploader_name": self.uploader.real_name if self.uploader else None,
            "related_report_id": self.related_report_id,
            "create_time": format_value(self.create_time),
            "update_time": format_value(self.update_time),
        }

