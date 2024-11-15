import uuid


def generate_id():
    return str(uuid.uuid4())


def object_id_to_str(data) -> dict[str, str]:
    data['id'] = str(data['_id'])
    del data['_id']
    return data