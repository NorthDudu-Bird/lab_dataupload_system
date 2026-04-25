from .base import TimestampMixin, format_value
from ..extensions import db


class LabInfo(db.Model, TimestampMixin):
    __tablename__ = "lab_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_code = db.Column(db.String(50), nullable=False, unique=True)
    lab_name = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100), nullable=False)
    room_no = db.Column(db.String(50), nullable=False)
    manager_name = db.Column(db.String(50))
    capacity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), nullable=False, default="enabled")
    remark = db.Column(db.String(500))

    equipments = db.relationship("LabEquipment", back_populates="lab", lazy="dynamic")
    reports = db.relationship("LabReport", back_populates="lab", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "lab_code": self.lab_code,
            "lab_name": self.lab_name,
            "building": self.building,
            "room_no": self.room_no,
            "manager_name": self.manager_name,
            "capacity": self.capacity,
            "status": self.status,
            "remark": self.remark,
            "create_time": format_value(self.create_time),
            "update_time": format_value(self.update_time),
        }

