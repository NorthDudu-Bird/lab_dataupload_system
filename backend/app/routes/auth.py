from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from ..common.exceptions import AppError
from ..common.response import success
from ..decorators.roles import get_current_user
from ..models.equipment import LabEquipment
from ..models.lab import LabInfo
from ..models.report import LabReport
from ..models.user import SysUser
from ..schemas.auth import LoginSchema


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    payload = LoginSchema().load(request.get_json() or {})
    user = SysUser.query.filter_by(username=payload["username"]).first()
    if not user or not check_password_hash(user.password, payload["password"]):
        raise AppError("用户名或密码错误", 401, 401)
    if user.status != "enabled":
        raise AppError("账号已被禁用，请联系管理员", 403, 403)

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "username": user.username},
    )
    return success({"token": token, "user": user.to_dict()})


@auth_bp.get("/profile")
def profile():
    user = get_current_user()
    return success(user.to_dict())


@auth_bp.get("/public-overview")
def public_overview():
    total = LabReport.query.count()
    pending = LabReport.query.filter(LabReport.review_status == "pending").count()
    approved = LabReport.query.filter(LabReport.review_status == "approved").count()
    rejected = LabReport.query.filter(LabReport.review_status == "rejected").count()
    abnormal = LabReport.query.filter(
        (LabReport.hygiene_status == "abnormal")
        | (LabReport.power_status == "abnormal")
        | (LabReport.network_status == "abnormal")
        | (LabReport.door_window_status == "abnormal")
        | (LabReport.fire_status == "abnormal")
        | (LabReport.equipment_status == "abnormal")
        | ((LabReport.abnormal_desc.isnot(None)) & (LabReport.abnormal_desc != ""))
    ).count()
    labs = LabInfo.query.count()
    equipments = LabEquipment.query.count()
    return success(
        {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "abnormal": abnormal,
            "labs": labs,
            "equipments": equipments,
        }
    )
