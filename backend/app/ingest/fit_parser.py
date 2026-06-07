"""NK FIT parser (later), via fitdecode."""

from ..models import Activity, Sample


def parse(content: bytes) -> tuple[Activity, list[Sample]]:
    # TODO: parse .fit into canonical Activity + Sample[] (fitdecode).
    raise NotImplementedError
