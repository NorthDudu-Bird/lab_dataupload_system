from datetime import date, timedelta

from flask import Blueprint
from sqlalchemy import func

from ..common.response import success
from ..decorators.roles import get_current_user, role_required
from ..models.equipment import LabEquipment
from ..models.lab import LabInfo
from ..models.report import LabReport


dashboard_bp = Blueprint("dashboard", __name__)


def _scoped_report_query(user):
    query = LabReport.query
    if user.role == "reporter":
        query = query.filter(LabReport.reporter_id == user.id)
    return query


@dashboard_bp.get("")
@role_required("admin", "reviewer", "reporter")
def dashboard():
    user = get_current_user()
    query = _scoped_report_query(user)
    total = query.count()
    pending = query.filter(LabReport.review_status == "pending").count()
    approved = query.filter(LabReport.review_status == "approved").count()
    rejected = query.filter(LabReport.review_status == "rejected").count()
    abnormal = query.filter(
        (LabReport.hygiene_status == "abnormal")
        | (LabReport.power_status == "abnormal")
        | (LabReport.network_status == "abnormal")
        | (LabReport.door_window_status == "abnormal")
        | (LabReport.fire_status == "abnormal")
        | (LabReport.equipment_status == "abnormal")
        | ((LabReport.abnormal_desc.isnot(None)) & (LabReport.abnormal_desc != ""))
    ).count()

    lab_query = (
        _scoped_report_query(user)
        .join(LabInfo, LabReport.lab_id == LabInfo.id)
        .with_entities(LabInfo.lab_name, func.count(LabReport.id))
        .group_by(LabInfo.id, LabInfo.lab_name)
        .all()
    )
    lab_stats = [{"name": name, "value": count} for name, count in lab_query]

    start_day = date.today() - timedelta(days=13)
    trend_rows = (
        _scoped_report_query(user)
        .with_entities(LabReport.report_date, func.count(LabReport.id))
        .filter(LabReport.report_date >= start_day)
        .group_by(LabReport.report_date)
        .order_by(LabReport.report_date.asc())
        .all()
    )
    trend_map = {row[0].strftime("%Y-%m-%d"): row[1] for row in trend_rows}
    trend = []
    for offset in range(14):
        day = start_day + timedelta(days=offset)
        day_key = day.strftime("%Y-%m-%d")
        trend.append({"date": day_key, "count": trend_map.get(day_key, 0)})

    device_rows = (
        LabEquipment.query.with_entities(LabEquipment.status, func.count(LabEquipment.id))
        .group_by(LabEquipment.status)
        .all()
    )
    device_status = [{"name": status, "value": count} for status, count in device_rows]

    return success(
        {
            "cards": {
                "total": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
                "abnormal": abnormal,
            },
            "lab_stats": lab_stats,
            "trend": trend,
            "device_status": device_status,
        }
    )
