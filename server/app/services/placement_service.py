from app.models.placement_history import PlacementHistory


def get_history_for_student(student_id):
    return (
        PlacementHistory.query
        .filter_by(student_id=student_id)
        .order_by(PlacementHistory.recorded_at.desc())
        .all()
    )


def get_all_history():
    return PlacementHistory.query.order_by(PlacementHistory.recorded_at.desc()).all()


def get_latest_status_for_student(student_id):
    """One row per drive: the most recent status for each drive the student applied to."""
    history = get_history_for_student(student_id)  # already newest-first
    latest_by_drive = {}
    for entry in history:
        if entry.drive_id not in latest_by_drive:
            latest_by_drive[entry.drive_id] = entry
    return list(latest_by_drive.values())
