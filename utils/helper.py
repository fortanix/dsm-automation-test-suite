import json
import uuid


def read_json(filepath, size=15):
    data = open(filepath, "r").read().replace("${random}", uuid.uuid4().hex[:size])
    return json.loads(data)
