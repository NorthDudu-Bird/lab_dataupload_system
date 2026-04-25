from flask import Blueprint, request

from ..common.response import success
from ..decorators.roles import role_required
from ..extensions import db
from ..models.lab import LabInfo
from ..schemas.lab import LabSchema


labs_bp = Blueprint("labs", __name__)


@labs_bp.get("")
@role_required("admin", "reviewer", "reporter")
def list_labs():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    query = LabInfo.query
    keyword = request.args.get("keyword")
    status = request.args.get("status")
    if keyword:
        query = query.filter((LabInfo.lab_code.like(f"%{keyword}%")) | (LabInfo.lab_name.like(f"%{keyword}%")))
    if status:
        query = query.filter(LabInfo.status == status)
    pagination = query.order_by(LabInfo.id.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return success({"items": [item.to_dict() for item in pagination.items], "total": pagination.total})


@labs_bp.post("")
@role_required("admin")
def create_lab():
    payload = LabSchema().load(request.get_json() or {})
    lab = LabInfo(**payload)
    db.session.add(lab)
    db.session.commit()
    return success(lab.to_dict(), "创建成功")


@labs_bp.put("/<int:lab_id>")
@role_required("admin")
def update_lab(lab_id):
    payload = LabSchema().load(request.get_json() or {})
    lab = LabInfo.query.get_or_404(lab_id)
    for key, value in payload.items():
        setattr(lab, key, value)
    db.session.commit()
    return success(lab.to_dict(), "更新成功")


@labs_bp.delete("/<int:lab_id>")
@role_required("admin")
def delete_lab(lab_id):
    lab = LabInfo.query.get_or_404(lab_id)
    db.session.delete(lab)
    db.session.commit()
    return success(message="删除成功")

