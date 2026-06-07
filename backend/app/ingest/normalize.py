"""Cross-source dedupe + canonical-model helpers."""

from ..models import Activity


def dedupe_key(activity: Activity) -> str:
    """Stable key to detect the same workout arriving from multiple sources.

    Prefer (source, external_id); fall back to start time rounded to the minute.
    TODO: add a content hash for file uploads with no external id.
    """
    if activity.external_id:
        return f"{activity.source}:{activity.external_id}"
    return f"start:{activity.start_time.replace(second=0, microsecond=0).isoformat()}"
