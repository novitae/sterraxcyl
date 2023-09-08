from typing import Any
from types import NoneType
import json
import uuid
import urllib.parse

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

def random_request_id(user_id: int) -> str:
    return "_".join([str(user_id), upper_uuid4()])

def sign(
    payload: dict = {},
    as_dict: bool = True
) -> dict | str:
    result = f"SIGNATURE.{flat_json_dumps(payload=payload)}"
    if as_dict is True:
        return {"signed_body": result}
    else:
        return result

def unsign(
    payload: dict | str
) -> dict:
    if isinstance(payload, dict):
        payload = payload["signed_body"]
    result = payload.split(".", 1)[1]
    result = urllib.parse.unquote(result)
    return json.loads(result)

def convert_headers(headers: dict[str, Any]) -> dict[str, str]:
    result = {}
    for key, value in headers.items():
        if isinstance(value, (int, float, bool)):
            value = str(value)
        elif isinstance(value, (list, dict, NoneType)):
            value = flat_json_dumps(value)
        result[key] = value
    return result