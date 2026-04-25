from datetime import datetime

from flask import Blueprint, request, send_from_directory

from ..common.exceptions import AppError
from ..common.response import success
from ..config import BASE_DIR
from ..decorators.roles import get_current_user, role_required
from ..extensions import db
from ..models.file import SysFile
from ..models.report import LabReport
from ..schemas.report import ReportSchema
from ..services.report_service import generate_report_no
from ..utils.file_helper import save_upload_file


reports_bp = Blueprint("reports", __name__)


def _apply_role_scope(query, user):
    if user.role == "reporter":
        return query.filter(LabReport.reporter_id == user.id)
    return query


def _get_accessible_report(report_id, user):
    report = LabReport.query.get_or_404(report_id)
    if user.role == "reporter" and report.reporter_id != user.id:
        raise AppError("无权访问该上报记录", 403, 403)
    return report


def _is_abnormal(report):
    fields = [
        report.hygiene_status,
        report.power_status,
        report.network_status,
        report.door_window_status,
        report.fire_status,
        report.equipment_status,
    ]
    return any(value == "abnormal" for value in fields) or bool(report.abnormal_desc)


@reports_bp.get("")
@role_required("admin", "reviewer", "reporter")
def list_reports():
    user = get_current_user()
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    query = _apply_role_scope(LabReport.query, user)

    lab_id = request.args.get("lab_id", type=int)
    reporter_id = request.args.get("reporter_id", type=int)
    review_status = request.args.get("review_status")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    keyword = request.args.get("keyword")
    abnormal = request.args.get("abnormal")

    if lab_id:
        query = query.filter(LabReport.lab_id == lab_id)
    if reporter_id and user.role in ["admin", "reviewer"]:
        query = query.filter(LabReport.reporter_id == reporter_id)
    if review_status:
        query = query.filter(LabReport.review_status == review_status)
    if start_date:
        query = query.filter(LabReport.report_date >= start_date)
    if end_date:
        query = query.filter(LabReport.report_date <= end_date)
    if keyword:
        query = query.filter(LabReport.report_no.like(f"%{keyword}%"))
    if abnormal == "1":
        query = query.filter(
            (LabReport.hygiene_status == "abnormal")
            | (LabReport.power_status == "abnormal")
            | (LabReport.network_status == "abnormal")
            | (LabReport.door_window_status == "abnormal")
            | (LabReport.fire_status == "abnormal")
            | (LabReport.equipment_status == "abnormal")
            | ((LabReport.abnormal_desc.isnot(None)) & (LabReport.abnormal_desc != ""))
        )

    pagination = query.order_by(LabReport.report_date.desc(), LabReport.id.desc()).paginate(
        page=page,
        per_page=page_size,
        error_out=False,
    )
    return success({"items": [item.to_dict() for item in pagination.items], "total": pagination.total})


@reports_bp.post("")
@role_required("admin", "reporter")
def create_report():
    user = get_current_user()
    payload = ReportSchema().load(request.get_json() or {})
    report = LabReport(
        report_no=generate_report_no(),
        reporter_id=user.id,
        review_status="pending",
        **payload,
    )
    db.session.add(report)
    db.session.commit()
    return success(report.to_dict(), "提交成功")


@reports_bp.get("/<int:report_id>")
@role_required("admin", "reviewer", "reporter")
def get_report(report_id):
    user = get_current_user()
    report = _get_accessible_report(report_id, user)
    data = report.to_dict()
    data["is_abnormal"] = _is_abnormal(report)
    return success(data)


@reports_bp.put("/<int:report_id>")
@role_required("admin", "reporter")
def update_report(report_id):
    user = get_current_user()
    report = _get_accessible_report(report_id, user)
    if report.review_status != "pending":
        raise AppError("已审核记录不能修改")
    if user.role == "reporter" and report.reporter_id != user.id:
        raise AppError("只能修改本人待审核的上报记录", 403, 403)

    payload = ReportSchema().load(request.get_json() or {})
    for key, value in payload.items():
        setattr(report, key, value)
    db.session.commit()
    return success(report.to_dict(), "更新成功")


@reports_bp.delete("/<int:report_id>")
@role_required("admin", "reporter")
def delete_report(report_id):
    user = get_current_user()
    report = _get_accessible_report(report_id, user)
    if user.role == "reporter" and report.review_status != "pending":
        raise AppError("只能删除本人待审核的上报记录", 403, 403)
    db.session.delete(report)
    db.session.commit()
    return success(message="删除成功")


@reports_bp.post("/upload")
@role_required("admin", "reviewer", "reporter")
def upload_file():
    user = get_current_user()
    file_storage = request.files.get("file")
    saved = save_upload_file(file_storage)
    record = SysFile(uploader_id=user.id, **saved)
    db.session.add(record)
    db.session.commit()
    return success(record.to_dict(), "上传成功")


@reports_bp.get("/files/<path:filename>")
def get_upload_file(filename):
    return send_from_directory(BASE_DIR / "uploads", filename, as_attachment=False)
