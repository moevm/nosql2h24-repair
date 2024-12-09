import uuid
from datetime import datetime, timezone


def generate_id():
    return str(uuid.uuid4())


def object_id_to_str(data) -> dict[str, str] | None:
    if data is None:
        return None
    data['id'] = str(data['_id'])
    del data['_id']
    return data


def get_date_now() -> datetime:
    return datetime.now(timezone.utc)
