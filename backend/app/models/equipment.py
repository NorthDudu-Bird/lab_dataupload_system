from .base import TimestampMixin, format_value
from ..extensions import db


class LabEquipment(db.Model, TimestampMixin):
    __tablename__ = "lab_equipment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipment_code = db.Column(db.String(50), nullable=False, unique=True)
    equipment_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(80))
    lab_id = db.Column(db.Integer, db.ForeignKey("lab_info.id"), nullable=False)
    purchase_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default="normal")
    remark = db.Column(db.String(500))

    lab = db.relationship("LabInfo", back_populates="equipments")

    def to_dict(self):
        return {
            "id": self.id,
            "equipment_code": self.equipment_code,
            "equipment_name": self.equipment_name,
            "category": self.category,
            "brand": self.brand,
            "model": self.model,
            "lab_id": self.lab_id,
            "lab_name": self.lab.lab_name if self.lab else None,
            "purchase_date": format_value(self.purchase_date),
            "status": self.status,
            "remark": self.remark,
            "create_time": format_value(self.create_time),
            "update_time": format_value(self.update_time),
        }

