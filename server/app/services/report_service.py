
import csv
import io
from collections import Counter, defaultdict

from app.models.placement_history import PlacementHistory
from app.models.drive import Drive
from app.models.user import User
from app.extensions import db


# ---------------------------------------------------------------------------
# Student export
# ---------------------------------------------------------------------------

def build_student_history_csv(student_id):
    """Returns a CSV string of one student's full placement history log."""
    rows = (
        db.session.query(PlacementHistory)
        .filter(PlacementHistory.student_id == student_id)
        .order_by(PlacementHistory.recorded_at.asc())
        .all()
    )

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["Drive Title", "Company", "Role Offered", "Status",
         "Package (CTC)", "Remarks", "Recorded At"]
    )

    for row in rows:
        drive = row.drive  # relationship, assumed defined on PlacementHistory
        company = drive.company.username if drive and drive.company else ""
        writer.writerow(
            [
                drive.title if drive else "",
                company,
                drive.role_offered if drive else "",
                row.status,
                row.package_ctc if row.package_ctc is not None else "",
                row.remarks or "",
                row.recorded_at.strftime("%Y-%m-%d %H:%M") if row.recorded_at else "",
            ]
        )

    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Admin monthly report
# ---------------------------------------------------------------------------

def build_admin_report_data(period_start, period_end):
    """Aggregates everything the monthly admin report needs for one period.
    period_start / period_end are date objects, inclusive range."""

    history_rows = (
        db.session.query(PlacementHistory)
        .filter(
            PlacementHistory.recorded_at >= period_start,
            PlacementHistory.recorded_at <= period_end,
        )
        .all()
    )

    drives_in_period = (
        db.session.query(Drive)
        .filter(Drive.created_at >= period_start, Drive.created_at <= period_end)
        .all()
    )

    drive_counts = Counter(d.status for d in drives_in_period)

    application_counts = Counter(row.status for row in history_rows)

    placements = []
    rejections = []
    packages = []
    company_hire_counts = Counter()

    for row in history_rows:
        drive = row.drive
        student = row.student
        company_name = drive.company.username if drive and drive.company else "Unknown"

        if row.status == "selected":
            placements.append(
                {
                    "student": student.username if student else "Unknown",
                    "drive": drive.title if drive else "Unknown",
                    "company": company_name,
                    "package_ctc": row.package_ctc,
                    "date": row.recorded_at.isoformat() if row.recorded_at else None,
                }
            )
            if row.package_ctc:
                packages.append(row.package_ctc)
            company_hire_counts[company_name] += 1

        elif row.status == "rejected":
            rejections.append(
                {
                    "student": student.username if student else "Unknown",
                    "drive": drive.title if drive else "Unknown",
                    "company": company_name,
                    "date": row.recorded_at.isoformat() if row.recorded_at else None,
                }
            )

    top_companies = [
        {"company": name, "hires": count}
        for name, count in company_hire_counts.most_common(5)
    ]

    return {
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "drive_counts": dict(drive_counts),
        "application_counts": dict(application_counts),
        "placements": placements,
        "rejections": rejections,
        "total_offers": len(placements),
        "avg_package": round(sum(packages) / len(packages), 2) if packages else 0,
        "highest_package": max(packages) if packages else 0,
        "top_companies": top_companies,
    }


def build_admin_report_csv(data):
    """Flattens build_admin_report_data() output into one sectioned CSV."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["Placement Portal — Monthly Report"])
    writer.writerow(["Period", f"{data['period_start']} to {data['period_end']}"])
    writer.writerow([])

    writer.writerow(["Summary"])
    writer.writerow(["Total Offers", data["total_offers"]])
    writer.writerow(["Average Package (CTC)", data["avg_package"]])
    writer.writerow(["Highest Package (CTC)", data["highest_package"]])
    writer.writerow([])

    writer.writerow(["Drive Status Breakdown"])
    for status, count in data["drive_counts"].items():
        writer.writerow([status, count])
    writer.writerow([])

    writer.writerow(["Application Status Breakdown"])
    for status, count in data["application_counts"].items():
        writer.writerow([status, count])
    writer.writerow([])

    writer.writerow(["Top Companies by Hires"])
    writer.writerow(["Company", "Hires"])
    for entry in data["top_companies"]:
        writer.writerow([entry["company"], entry["hires"]])
    writer.writerow([])

    writer.writerow(["Placements"])
    writer.writerow(["Student", "Drive", "Company", "Package (CTC)", "Date"])
    for p in data["placements"]:
        writer.writerow([p["student"], p["drive"], p["company"], p["package_ctc"], p["date"]])
    writer.writerow([])

    writer.writerow(["Rejections"])
    writer.writerow(["Student", "Drive", "Company", "Date"])
    for r in data["rejections"]:
        writer.writerow([r["student"], r["drive"], r["company"], r["date"]])

    return buffer.getvalue()