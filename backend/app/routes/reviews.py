from datetime import datetime

from flask import Blueprint, request

from ..common.exceptions import AppError
from ..common.response import success
from ..decorators.roles import get_current_user, role_required
from ..extensions import db
from ..models.report import LabReport
from ..schemas.report import ReviewSchema


reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.get("")
@role_required("admin", "reviewer")
def list_review_reports():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    review_status = request.args.get("review_status", "pending")
    query = LabReport.query
    if review_status:
        query = query.filter(LabReport.review_status == review_status)
    pagination = query.order_by(LabReport.report_date.desc(), LabReport.id.desc()).paginate(
        page=page,
        per_page=page_size,
        error_out=False,
    )
    return success({"items": [item.to_dict() for item in pagination.items], "total": pagination.total})


@reviews_bp.post("/<int:report_id>/audit")
@role_required("admin", "reviewer")
def audit_report(report_id):
    user = get_current_user()
    payload = ReviewSchema().load(request.get_json() or {})
    report = LabReport.query.get_or_404(report_id)
    if report.review_status != "pending":
        raise AppError("该记录已审核，不能重复审核")
    report.review_status = payload["review_status"]
    report.review_comment = payload["review_comment"]
    report.reviewer_id = user.id
    report.review_time = datetime.now()
    db.session.commit()
    return success(report.to_dict(), "审核完成")

