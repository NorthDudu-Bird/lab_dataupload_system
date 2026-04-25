from .base import TimestampMixin, format_value
from ..extensions import db


class LabReport(db.Model, TimestampMixin):
    __tablename__ = "lab_report"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_no = db.Column(db.String(50), nullable=False, unique=True)
    report_date = db.Column(db.Date, nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey("lab_info.id"), nullable=False)
    reporter_id = db.Column(db.Integer, db.ForeignKey("sys_user.id"), nullable=False)
    temperature = db.Column(db.Numeric(5, 2))
    humidity = db.Column(db.Numeric(5, 2))
    hygiene_status = db.Column(db.String(20), nullable=False)
    power_status = db.Column(db.String(20), nullable=False)
    network_status = db.Column(db.String(20), nullable=False)
    door_window_status = db.Column(db.String(20), nullable=False)
    fire_status = db.Column(db.String(20), nullable=False)
    equipment_status = db.Column(db.String(20), nullable=False)
    usage_count = db.Column(db.Integer, nullable=False, default=0)
    abnormal_desc = db.Column(db.Text)
    attachment_path = db.Column(db.String(255))
    review_status = db.Column(db.String(20), nullable=False, default="pending")
    review_comment = db.Column(db.String(500))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("sys_user.id"))
    review_time = db.Column(db.DateTime)

    lab = db.relationship("LabInfo", back_populates="reports")
    reporter = db.relationship("SysUser", foreign_keys=[reporter_id])
    reviewer = db.relationship("SysUser", foreign_keys=[reviewer_id])

    def to_dict(self):
        return {
            "id": self.id,
            "report_no": self.report_no,
            "report_date": format_value(self.report_date),
            "lab_id": self.lab_id,
            "lab_name": self.lab.lab_name if self.lab else None,
            "reporter_id": self.reporter_id,
            "reporter_name": self.reporter.real_name if self.reporter else None,
            "temperature": float(self.temperature) if self.temperature is not None else None,
            "humidity": float(self.humidity) if self.humidity is not None else None,
            "hygiene_status": self.hygiene_status,
            "power_status": self.power_status,
            "network_status": self.network_status,
            "door_window_status": self.door_window_status,
            "fire_status": self.fire_status,
            "equipment_status": self.equipment_status,
            "usage_count": self.usage_count,
            "abnormal_desc": self.abnormal_desc,
            "attachment_path": self.attachment_path,
            "review_status": self.review_status,
            "review_comment": self.review_comment,
            "reviewer_id": self.reviewer_id,
            "reviewer_name": self.reviewer.real_name if self.reviewer else None,
            "review_time": format_value(self.review_time),
            "create_time": format_value(self.create_time),
            "update_time": format_value(self.update_time),
        }

