from datetime import datetime

from flask import Blueprint, request

from ..common.response import success
from ..decorators.roles import get_current_user, role_required
from ..extensions import db
from ..models.notice import SysNotice
from ..schemas.notice import NoticeSchema


notices_bp = Blueprint("notices", __name__)


@notices_bp.get("")
@role_required("admin", "reviewer", "reporter")
def list_notices():
    user = get_current_user()
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    keyword = request.args.get("keyword")
    status = request.args.get("status")
    query = SysNotice.query
    if user.role != "admin":
        query = query.filter(SysNotice.status == "published")
    elif status:
        query = query.filter(SysNotice.status == status)
    if keyword:
        query = query.filter(SysNotice.title.like(f"%{keyword}%"))
    pagination = query.order_by(SysNotice.published_time.desc(), SysNotice.id.desc()).paginate(
        page=page,
        per_page=page_size,
        error_out=False,
    )
    return success({"items": [item.to_dict() for item in pagination.items], "total": pagination.total})


@notices_bp.post("")
@role_required("admin")
def create_notice():
    user = get_current_user()
    payload = NoticeSchema().load(request.get_json() or {})
    notice = SysNotice(
        publisher_id=user.id,
        published_time=datetime.now() if payload["status"] == "published" else None,
        **payload,
    )
    db.session.add(notice)
    db.session.commit()
    return success(notice.to_dict(), "发布成功")


@notices_bp.put("/<int:notice_id>")
@role_required("admin")
def update_notice(notice_id):
    payload = NoticeSchema().load(request.get_json() or {})
    notice = SysNotice.query.get_or_404(notice_id)
    old_status = notice.status
    notice.title = payload["title"]
    notice.content = payload["content"]
    notice.status = payload["status"]
    if old_status != "published" and notice.status == "published":
        notice.published_time = datetime.now()
    db.session.commit()
    return success(notice.to_dict(), "更新成功")


@notices_bp.delete("/<int:notice_id>")
@role_required("admin")
def delete_notice(notice_id):
    notice = SysNotice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    return success(message="删除成功")

