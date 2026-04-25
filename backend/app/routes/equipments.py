from flask import Blueprint, request

from ..common.response import success
from ..decorators.roles import role_required
from ..extensions import db
from ..models.equipment import LabEquipment
from ..schemas.equipment import EquipmentSchema


equipments_bp = Blueprint("equipments", __name__)


@equipments_bp.get("")
@role_required("admin", "reviewer", "reporter")
def list_equipments():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    query = LabEquipment.query
    keyword = request.args.get("keyword")
    lab_id = request.args.get("lab_id", type=int)
    status = request.args.get("status")
    category = request.args.get("category")

    if keyword:
        query = query.filter(
            (LabEquipment.equipment_code.like(f"%{keyword}%"))
            | (LabEquipment.equipment_name.like(f"%{keyword}%"))
        )
    if lab_id:
        query = query.filter(LabEquipment.lab_id == lab_id)
    if status:
        query = query.filter(LabEquipment.status == status)
    if category:
        query = query.filter(LabEquipment.category == category)

    pagination = query.order_by(LabEquipment.id.desc()).paginate(
        page=page,
        per_page=page_size,
        error_out=False,
    )
    return success({"items": [item.to_dict() for item in pagination.items], "total": pagination.total})


@equipments_bp.post("")
@role_required("admin")
def create_equipment():
    payload = EquipmentSchema().load(request.get_json() or {})
    equipment = LabEquipment(**payload)
    db.session.add(equipment)
    db.session.commit()
    return success(equipment.to_dict(), "创建成功")


@equipments_bp.put("/<int:equipment_id>")
@role_required("admin")
def update_equipment(equipment_id):
    payload = EquipmentSchema().load(request.get_json() or {})
    equipment = LabEquipment.query.get_or_404(equipment_id)
    for key, value in payload.items():
        setattr(equipment, key, value)
    db.session.commit()
    return success(equipment.to_dict(), "更新成功")


@equipments_bp.delete("/<int:equipment_id>")
@role_required("admin")
def delete_equipment(equipment_id):
    equipment = LabEquipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    return success(message="删除成功")

