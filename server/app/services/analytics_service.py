# backend/app/services/analytics_service.py
#
# Powers the live "Analytics" tab in AdminDashboard.vue. Computed on request
# rather than cached, so it always reflects current data. Separate from
# report_service, which builds the point-in-time monthly snapshot.

from collections import Counter
from datetime import date
from dateutil.relativedelta import relativedelta

from app.models.drive import Drive
from app.models.placement_history import PlacementHistory
from app.extensions import db


def get_dashboard_analytics(months_back=6):
    drive_status_breakdown = _drive_status_breakdown()
    application_status_breakdown = _application_status_breakdown()
    placement_trend = _placement_trend(months_back)
    top_companies = _top_companies()

    return {
        "drive_status_breakdown": drive_status_breakdown,
        "application_status_breakdown": application_status_breakdown,
        "placement_trend": placement_trend,
        "top_companies": top_companies,
    }


def _drive_status_breakdown():
    rows = db.session.query(Drive.status).all()
    counts = Counter(r[0] for r in rows)
    return {
        "pending": counts.get("pending", 0),
        "approved": counts.get("approved", 0),
        "rejected": counts.get("rejected", 0),
    }


def _application_status_breakdown():
    # Latest status per (student, drive) — reuse the same "collapse the log"
    # logic as placement_service.get_latest_status_for_student, but unfiltered.
    latest_per_pair = {}
    rows = (
        db.session.query(PlacementHistory)
        .order_by(PlacementHistory.recorded_at.asc())
        .all()
    )
    for row in rows:
        latest_per_pair[(row.student_id, row.drive_id)] = row.status

    counts = Counter(latest_per_pair.values())
    return {
        "applied": counts.get("applied", 0),
        "shortlisted": counts.get("shortlisted", 0),
        "interview": counts.get("interview", 0),
        "selected": counts.get("selected", 0),
        "rejected": counts.get("rejected", 0),
    }


def _placement_trend(months_back):
    today = date.today()
    start = today.replace(day=1) - relativedelta(months=months_back - 1)

    rows = (
        db.session.query(PlacementHistory)
        .filter(
            PlacementHistory.status == "selected",
            PlacementHistory.recorded_at >= start,
        )
        .all()
    )

    buckets = {}
    cursor = start
    for _ in range(months_back):
        key = cursor.strftime("%Y-%m")
        buckets[key] = {"placed": 0, "total_ctc": 0}
        cursor += relativedelta(months=1)

    for row in rows:
        key = row.recorded_at.strftime("%Y-%m")
        if key in buckets:
            buckets[key]["placed"] += 1
            buckets[key]["total_ctc"] += row.package_ctc or 0

    trend = []
    for month, values in buckets.items():
        avg_ctc = round(values["total_ctc"] / values["placed"], 2) if values["placed"] else 0
        trend.append({"month": month, "placed": values["placed"], "avg_ctc": avg_ctc})

    return trend


def _top_companies(limit=5):
    rows = (
        db.session.query(PlacementHistory)
        .filter(PlacementHistory.status == "selected")
        .all()
    )
    counts = Counter()
    for row in rows:
        drive = row.drive
        name = drive.company.username if drive and drive.company else "Unknown"
        counts[name] += 1

    return [{"company": name, "hires": count} for name, count in counts.most_common(limit)]