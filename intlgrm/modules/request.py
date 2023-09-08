import urllib.parse
import json
from furl import furl
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .authorization import Authorization
    from .headers import Headers
else:
    class Authorization: pass
    class Headers: pass

from .. import utils

def sign(
    payload: dict = {},
    as_dict: bool = True
) -> dict | str:
    result = f"SIGNATURE.{utils.flat_json_dumps(payload=payload)}"
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


def request(
    headers: Headers,
    method: str,
    url: str,
    params: dict,
    data: dict | None = None,
    content_type = None,
    auth: Authorization = None,
    language: str = None,
    ignore_headers: set[str] = None,
    manual_headers: dict = {},
) -> dict:
    nurl = furl(url)
    if not nurl.scheme:
        if not url.startswith('/api/v1'):
            url = '/api/v1' + url
    url = furl('https://i.instagram.com' + url).url

    if language is not None:
        params.setdefault("hl", language)

    headersd = headers.to_headers(
        auth=auth,
        has_body=method != "GET" and data is not None,
        content_type=content_type,
        ignore_headers=ignore_headers,
    )
    headersd.update(manual_headers)
    return {
        "method": method,
        "url": url,
        "headers": headersd,
        "params": params,
        **({"data": data} if data else {})
    }

def get(
    headers: Headers,
    endpoint: str,
    params: dict = None,
    auth: Headers = None,
    include_device_id: bool = False,
    request_id_name: str = None,
    language: str = None,
    ignore_headers: set[str] = set(),
    manual_headers: dict = {},
) -> dict:
    if any([params, include_device_id, request_id_name]):
        if params:
            assert isinstance(params, dict)
        else:
            params = {}
        if include_device_id is True:
            params.setdefault('device_id', headers.deviceid.device_id)
        if request_id_name is not None:
            params.setdefault(request_id_name, random_request_id())
    return request(
        headers=Headers,
        method="GET",
        url=endpoint,
        params=params,
        auth=auth,
        language=language,
        ignore_headers=ignore_headers,
        manual_headers=manual_headers,
    )

def media(
    headers: Headers,
    url: str,
    name: str,
) -> dict:
    return {
        "method": "GET",
        "url": url,
        "headers": {
            "X-FB-Friendly-Name": "video" if name.endswith(".mp4") else "image-media",
            "User-Agent": str(headers.user_agent),
            "X-IG-Bandwidth-Speed-KBPS": "0.000",
            "X-FB-Connection-Type": "wifi",
            "Accept-Language": headers.language.language,
            "X-Tigon-Is-Retry": "False",
            "Priority": "u=2, i",
            "Accept-Encoding": "x-fb-dz;d=2, zstd, gzip, deflate",
            "Liger": "X-FB-HTTP-Engine",
            "X-FB-Client-IP": "True",
            "X-FB-Server-Cluster": "True",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
    }

async def post(
    headers: Headers,
    endpoint: str,
    params: dict = {},
    data: dict = None,
    skip_signing: bool = False,
    content_type: str = None,
    auth: Authorization = None,
    include_uuid: bool = False,
    include_uid: bool = False,
    include_device_id: bool = False,
    include_phone_id: bool = False,
    include_family_device_id: bool = False,
    request_id_name: str = None,
    language: str = None,
    ignore_headers: set[str] = set(),
    manual_headers: dict = {},
) -> dict:
    if any([
        data, request_id_name,
        include_uuid, include_device_id, include_phone_id,
        include_uid, include_family_device_id
    ]):
        if data is None:
            data = {}
        else:
            assert isinstance(data, dict)
        if request_id_name is not None:
            data.setdefault(request_id_name, random_request_id())
        if include_uuid:
            data.setdefault('_uuid', headers.deviceid.device_id)
        if include_device_id:
            data.setdefault('device_id', headers.deviceid.device_id)
        if include_phone_id:
            data.setdefault('phone_id', headers.deviceid.device_id)
        if include_family_device_id:
            data.setdefault('family_device_id', headers.deviceid.device_id)
        if include_uid and auth:
            data.setdefault('_uid', str(auth.user_id))
        data = data if skip_signing else sign(payload=data)

    return request(
        headers=headers,
        method="POST",
        url=endpoint,
        data=data,
        content_type=content_type,
        params=params,
        auth=auth,
        language=language,
        ignore_headers=ignore_headers,
        manual_headers=manual_headers,
    )

def bloks(
    headers: Headers,
    app: str,
    payload: dict = {},
    language: str = None,
    blok_id: str = None,
    auth: Authorization = None,
    ignore_headers: set[str] = None,
    manual_headers: dict = {},
) -> dict:
    return post(
        headers=headers,
        endpoint=f"/bloks/apps/{app}/",
        data={"bloks_versioning_id": blok_id, **payload},
        auth=auth,
        include_uuid=True,
        include_uid=True,
        language=language,
        ignore_headers=ignore_headers,
        manual_headers=manual_headers,
    )

def random_request_id(auth: Authorization) -> str:
    return "_".join([str(auth.user_id), utils.upper_uuid4()])