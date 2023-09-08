from typing import Any
import json
import uuid

def flat_json_dumps(
    payload: Any
) -> str:
    return json.dumps(
        payload,
        separators=(",", ":")
    )

def str_uuid4() -> str:
    return uuid.uuid4().__str__()

def upper_uuid4() -> str:
    return str_uuid4().upper()
