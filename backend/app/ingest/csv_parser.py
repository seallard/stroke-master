"""NK SpeedCoach CSV parser (later). Full per-stroke fidelity."""

from ..models import Activity, Sample


def parse(content: bytes) -> tuple[Activity, list[Sample]]:
    # TODO: parse NK SpeedCoach CSV export into canonical Activity + Sample[].
    raise NotImplementedError
