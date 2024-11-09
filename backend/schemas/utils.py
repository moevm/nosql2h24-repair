import uuid


def generate_id():
    return str(uuid.uuid4())


def object_id_to_str(user) -> dict[str, str]:
    user['id'] = str(user['_id'])
    return user