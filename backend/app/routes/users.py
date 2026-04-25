from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from ..common.exceptions import AppError
from ..common.response import success
from ..decorators.roles import get_current_user, role_required
from ..extensions import db
from ..models.user import SysUser
from ..schemas.user import ResetPasswordSchema, UserCreateSchema, UserStatusSchema, UserUpdateSchema


users_bp = Blueprint("users", __name__)


@users_bp.get("")
@role_required("admin")
def list_users():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    query = SysUser.query
    username = request.args.get("username")
    real_name = request.args.get("real_name")
    role = request.args.get("role")
    status = request.args.get("status")

    if username:
        query = query.filter(SysUser.username.like(f"%{username}%"))
    if real_name:
        query = query.filter(SysUser.real_name.like(f"%{real_name}%"))
    if role:
        query = query.filter(SysUser.role == role)
    if status:
        query = query.filter(SysUser.status == status)

    pagination = query.order_by(SysUser.id.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return success({"items": [item.to_dict() for item in pagination.items], "total": pagination.total})


@users_bp.post("")
@role_required("admin")
def create_user():
    payload = UserCreateSchema().load(request.get_json() or {})
    if SysUser.query.filter_by(username=payload["username"]).first():
        raise AppError("用户名已存在")
    user = SysUser(
        username=payload["username"],
        password=generate_password_hash(payload["password"]),
        real_name=payload["real_name"],
        phone=payload.get("phone"),
        email=payload.get("email"),
        role=payload["role"],
        status=payload["status"],
    )
    db.session.add(user)
    db.session.commit()
    return success(user.to_dict(), "创建成功")


@users_bp.put("/<int:user_id>")
@role_required("admin")
def update_user(user_id):
    payload = UserUpdateSchema().load(request.get_json() or {})
    user = SysUser.query.get_or_404(user_id)
    user.real_name = payload["real_name"]
    user.phone = payload.get("phone")
    user.email = payload.get("email")
    user.role = payload["role"]
    user.status = payload["status"]
    db.session.commit()
    return success(user.to_dict(), "更新成功")


@users_bp.delete("/<int:user_id>")
@role_required("admin")
def delete_user(user_id):
    current_user = get_current_user()
    if current_user.id == user_id:
        raise AppError("不能删除当前登录账号")
    user = SysUser.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return success(message="删除成功")


@users_bp.patch("/<int:user_id>/status")
@role_required("admin")
def change_user_status(user_id):
    current_user = get_current_user()
    payload = UserStatusSchema().load(request.get_json() or {})
    if current_user.id == user_id and payload["status"] == "disabled":
        raise AppError("不能禁用当前登录账号")
    user = SysUser.query.get_or_404(user_id)
    user.status = payload["status"]
    db.session.commit()
    return success(user.to_dict(), "状态更新成功")


@users_bp.patch("/<int:user_id>/password/reset")
@role_required("admin")
def reset_password(user_id):
    payload = ResetPasswordSchema().load(request.get_json() or {})
    user = SysUser.query.get_or_404(user_id)
    user.password = generate_password_hash(payload["password"])
    db.session.commit()
    return success({"default_password": payload["password"]}, "密码重置成功")

