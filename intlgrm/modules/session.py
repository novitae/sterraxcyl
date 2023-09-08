from furl import furl
from typing import Literal, Any, AnyStr
from httpx import AsyncClient, Response
import json

from . import authorization, headers as _hders
from .. import utils

class InstagramResponse:
    def __init__(
        self,
        response: Response,
    ) -> None:
        self.response = response
        self.content_type: str = response.headers.get("Content-Type", "")
        try:
            self.dict: dict[AnyStr, Any] = response.json()
            self.is_json = True
        except json.JSONDecodeError:
            self.dict = None
            self.is_json = False

        if self.content_type.startswith(("video", "image")):
            self.status = self.status_code in (200, 206)
        else:
            self.status = self.dict.get("status") == "ok" if self.is_json else False

    def __repr__(self) -> str:
        return f"InstagramResponse(status: {self.status}, json: {self.is_json})"

    @property
    def status_code(self) -> int:
        return self.response.status_code
    
    def update_dyn_headers(
        self,
        user_session: "UserSession"
    ) -> None:
        user_session.headers.dyn_headers.update(self.response.headers)

class UserSession:
    def __init__(
        self,
        auth: authorization.Authorization = None,
        headers: _hders.Headers = None,
        client: AsyncClient = None
    ) -> None:
        self.auth = auth
        self.headers = headers or _hders.Headers()
        self.client = client or AsyncClient()

    def request_kwargs(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        api_version: Literal[1, 2] = None,
        data: dict | None = None,
        content_type: str = None,
        authorize: bool = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
    ) -> dict:
        """Returns the kwargs for a request.

        Args:
            method (str): Method to do request with.
            endpoint (str): Endpoint to get.
            params (dict, optional): Params to send with the request. Defaults to None.
            api_version (int, optional): Api version. Defaults to None.
            data (dict | None, optional): Data to post. Defaults to None.
            content_type (str, optional): Content type, will be set automatically if not precised. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to None.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.

        Returns:
            dict: kwargs as `{"method": "...", "url": "...", "params": {...}, "headers": {...}, "data": "..."}`
        """
        nurl = furl(endpoint)
        if not nurl.scheme:
            if not endpoint.startswith('/api/v'):
                url = f'/api/v{api_version or 1}' + ("" if endpoint.startswith("/") else "/") + endpoint
        url = furl('https://i.instagram.com' + url).url

        if language is not None:
            if params is None:
                params = {}
            params.setdefault("hl", language)

        headersd = self.headers.to_headers(
            auth=self.auth if (authorize or True) else None,
            has_body=method != "GET" and data is not None,
            content_type=content_type,
            ignore_headers=(ignore_headers or set()),
        )
        headersd.update(manual_headers or {})
        headersd = utils.convert_headers(headersd)
        return {
            "method": method,
            "url": url,
            "headers": headersd,
            "params": params or None,
            "data": data or None
        }

    def get_kwargs(
        self,
        endpoint: str,
        params: dict = None,
        api_version: Literal[1, 2] = None,
        authorize: bool = None,
        include_device_id: bool = False,
        request_id: str = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
    ) -> dict:
        """Returns the kwargs for a GET request.

        Args:
            endpoint (str): Endpoint to get.
            params (dict, optional): Params to send with the request. Defaults to None.
            api_version (int, optional): Api version. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to None.
            include_device_id (bool, optional): Include in data the key "device_id" and its value. Defaults to False.
            request_id (str, optional): A custom request id to use. Will be generated automatically otherwise. Defaults to None.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.

        Returns:
            dict: kwargs as `{"method": "...", "url": "...", "params": {...}, "headers": {...}, "data": "..."}`
        """
        if any([params, include_device_id, request_id]):
            if params:
                assert isinstance(params, dict)
            else:
                params = {}
            if include_device_id:
                params.setdefault('device_id', self.headers.deviceid.device_id)
            if request_id is not None:
                params.setdefault(request_id, utils.random_request_id())
        return self.request_kwargs(
            method="GET",
            endpoint=endpoint,
            api_version=api_version,
            params=params,
            authorize=authorize,
            language=language,
            ignore_headers=ignore_headers,
            manual_headers=manual_headers,
        )

    def post_kwargs(
        self,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        api_version: Literal[1, 2] = None,
        skip_signing: bool = None,
        content_type: str = None,
        authorize: bool = None,
        include_uuid: bool = False,
        include_uid: bool = False,
        include_device_id: bool = False,
        include_phone_id: bool = False,
        include_family_device_id: bool = False,
        request_id: str = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
    ) -> dict:
        """Returns the kwargs for a POST request.

        Args:
            endpoint (str): Endpoint to post to.
            params (dict, optional): Params to send with the request. Defaults to None.
            data (dict, optional): Data to post. Defaults to None.
            api_version (int, optional): Api version. Defaults to None.
            skip_signing (bool, optional): Skip request signing, and sending a form of the data instead of the signed form. Defaults to None.
            content_type (str, optional): Content type, will be set automatically if not precised. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to None.
            include_uuid (bool, optional): Include in data the key "uuid" and its value. Defaults to False.
            include_uid (bool, optional): Include in data the key "uid" and its value. Defaults to False.
            include_device_id (bool, optional): Include in data the key "device_id" and its value. Defaults to False.
            include_phone_id (bool, optional): Include in data the key "phone_id" and its value. Defaults to False.
            include_family_device_id (bool, optional): Include in data the key "family_device_id" and its value. Defaults to False.
            request_id (str, optional): A custom request id to use. Will be generated automatically otherwise. Defaults to None.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.

        Returns:
            dict: kwargs as `{"method": "...", "url": "...", "params": {...}, "headers": {...}, "data": "..."}`
        """
        if any([
            data, request_id,
            include_uuid, include_device_id, include_phone_id,
            include_uid, include_family_device_id
        ]):
            if data is None:
                data = {}
            else:
                assert isinstance(data, dict)
            if request_id is not None:
                data.setdefault(request_id, utils.random_request_id())
            if include_uuid:
                data.setdefault('_uuid', self.headers.deviceid.device_id)
            if include_device_id:
                data.setdefault('device_id', self.headers.deviceid.device_id)
            if include_phone_id:
                data.setdefault('phone_id', self.headers.deviceid.device_id)
            if include_family_device_id:
                data.setdefault('family_device_id', self.headers.deviceid.device_id)
            if include_uid and self.auth:
                data.setdefault('_uid', str(self.auth.user_id))
            data = data if (skip_signing or False) else utils.sign(payload=data)

        return self.request_kwargs(
            self,
            method="POST",
            endpoint=endpoint,
            api_version=api_version,
            data=data,
            content_type=content_type,
            params=params,
            authorize=authorize,
            language=language,
            ignore_headers=ignore_headers,
            manual_headers=manual_headers,
        )

    def media_kwargs(
        self,
        url: str,
    ) -> dict:
        """Returns the kwargs for a GET request to media.

        Args:
            url (str): Full url of the media to get.

        Returns:
            dict: kwargs as `{"method": "...", "url": "...", "headers": {...}}`
        """
        return {
            "method": "GET",
            "url": url,
            "headers": {
                "X-FB-Friendly-Name": "video" if furl(url).path.segments[-1].endswith(".mp4") else "image-media",
                "User-Agent": str(self.headers.user_agent),
                "X-IG-Bandwidth-Speed-KBPS": f"{self.headers.stats.bandwidth_speed:.3f}",
                "X-FB-Connection-Type": self.headers.stats.connection_type.lower(),
                "Accept-Language": self.headers.language.language,
                "X-Tigon-Is-Retry": "False",
                "Priority": "u=2, i",
                "Accept-Encoding": "gzip, deflate",
                "Liger": "X-FB-HTTP-Engine",
                "X-FB-Client-IP": "True",
                "X-FB-Server-Cluster": "True",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            }
        }

    def bloks_kwargs(
        self,
        app: str,
        payload: dict = None,
        blok_id: str = None,
        authorize: bool = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
    ) -> dict:
        """Returns the kwargs for a blok request.

        Args:
            app (str): Blok app name, ex: `com.bloks.www.ig.about_this_account`
            payload (dict, optional): Payload to send. Do not include "bloks_versioning_id", it is automatically added. Defaults to {}.
            blok_id (str, optional): Blok id, ex: `456a06cb008a2f6d72f04e94d26242d4607e80d5cf8d9a5aa34ec109117071c6`. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to True.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.

        Returns:
            dict: kwargs as `{"method": "...", "url": "...", "params": {...}, "headers": {...}, "data": "..."}`
        """
        return self.post_kwargs(
            endpoint=f"/bloks/apps/{app}/",
            data={"bloks_versioning_id": blok_id, **(payload or {})},
            authorize=authorize,
            include_uuid=True,
            include_uid=True,
            language=language,
            ignore_headers=ignore_headers,
            manual_headers=manual_headers,
        )

    async def _request(
        self,
        *args,
        **kwargs
    ) -> InstagramResponse:
        response = await self.client.request(*args, **kwargs)
        result = InstagramResponse(response)
        result.update_dyn_headers(self)
        return result

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        api_version: Literal[1, 2] = None,
        data: dict | None = None,
        content_type: str = None,
        authorize: bool = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
        **kwargs,
    ) -> InstagramResponse:
        """Returns an InstagramResponse of the request.

        Args:
            method (str): Method to do request with.
            endpoint (str): Endpoint to get.
            params (dict, optional): Params to send with the request. Defaults to None.
            api_version (int, optional): Api version. Defaults to None.
            data (dict | None, optional): Data to post. Defaults to None.
            content_type (str, optional): Content type, will be set automatically if not precised. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to None.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.
            **kwargs: Arguments that will be passed to the `AsyncClient(...).request` method.

        Returns:
            InstagramResponse
        """
        return await self._request(
            **self.request_kwargs(
                method=method,
                endpoint=endpoint,
                params=params,
                api_version=api_version,
                data=data,
                content_type=content_type,
                authorize=authorize,
                language=language,
                ignore_headers=ignore_headers,
                manual_headers=manual_headers,
            ),
            **kwargs,
        )
    
    async def get(
        self,
        endpoint: str,
        params: dict = None,
        api_version: Literal[1, 2] = None,
        authorize: bool = None,
        include_device_id: bool = False,
        request_id: str = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
        **kwargs
    ) -> InstagramResponse:
        """Returns an InstagramResponse of a GET request.

        Args:
            endpoint (str): Endpoint to get.
            params (dict, optional): Params to send with the request. Defaults to None.
            api_version (int, optional): Api version. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to None.
            include_device_id (bool, optional): Include in data the key "device_id" and its value. Defaults to False.
            request_id (str, optional): A custom request id to use. Will be generated automatically otherwise. Defaults to None.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.
            **kwargs: Arguments that will be passed to the `AsyncClient(...).request` method.

        Returns:
            InstagramResponse
        """
        return await self._request(
            **self.get_kwargs(
                endpoint=endpoint,
                params=params,
                api_version=api_version,
                authorize=authorize,
                include_device_id=include_device_id,
                request_id=request_id,
                language=language,
                ignore_headers=ignore_headers,
                manual_headers=manual_headers,
            ),
            **kwargs,
        )
    
    async def post_kwargs(
        self,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        api_version: Literal[1, 2] = None,
        skip_signing: bool = None,
        content_type: str = None,
        authorize: bool = None,
        include_uuid: bool = False,
        include_uid: bool = False,
        include_device_id: bool = False,
        include_phone_id: bool = False,
        include_family_device_id: bool = False,
        request_id: str = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
        **kwargs,
    ) -> InstagramResponse:
        """Returns an InstagramResponse of a POST request.

        Args:
            endpoint (str): Endpoint to post to.
            params (dict, optional): Params to send with the request. Defaults to None.
            data (dict, optional): Data to post. Defaults to None.
            api_version (int, optional): Api version. Defaults to None.
            skip_signing (bool, optional): Skip request signing, and sending a form of the data instead of the signed form. Defaults to None.
            content_type (str, optional): Content type, will be set automatically if not precised. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to None.
            include_uuid (bool, optional): Include in data the key "uuid" and its value. Defaults to False.
            include_uid (bool, optional): Include in data the key "uid" and its value. Defaults to False.
            include_device_id (bool, optional): Include in data the key "device_id" and its value. Defaults to False.
            include_phone_id (bool, optional): Include in data the key "phone_id" and its value. Defaults to False.
            include_family_device_id (bool, optional): Include in data the key "family_device_id" and its value. Defaults to False.
            request_id (str, optional): A custom request id to use. Will be generated automatically otherwise. Defaults to None.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.
            **kwargs: Arguments that will be passed to the `AsyncClient(...).request` method.

        Returns:
            InstagramResponse
        """
        return await self._request(
            **self.post_kwargs(
                endpoint=endpoint,
                params=params,
                data=data,
                api_version=api_version,
                skip_signing=skip_signing,
                content_type=content_type,
                authorize=authorize,
                include_uuid=include_uuid,
                include_uid=include_uid,
                include_device_id=include_device_id,
                include_phone_id=include_phone_id,
                include_family_device_id=include_family_device_id,
                request_id=request_id,
                language=language,
                ignore_headers=ignore_headers,
                manual_headers=manual_headers,
            ),
            **kwargs
        )
    
    async def media(
        self,
        url: str,
        **kwargs,
    ) -> InstagramResponse:
        """Returns an InstagramResponse of a GET request to media.

        Args:
            url (str): Full url of the media to get.
            **kwargs: Arguments that will be passed to the `AsyncClient(...).request` method.

        Returns:
            InstagramResponse
        """
        return await self._request(
            **self.media_kwargs(
                url=url
            ),
            **kwargs
        )

    async def bloks(
        self,
        app: str,
        payload: dict = None,
        blok_id: str = None,
        authorize: bool = None,
        language: str = None,
        ignore_headers: set[str] = None,
        manual_headers: dict = None,
        **kwargs,
    ) -> InstagramResponse:
        """Returns an InstagramResponse of a blok request.

        Args:
            app (str): Blok app name, ex: `com.bloks.www.ig.about_this_account`
            payload (dict, optional): Payload to send. Do not include "bloks_versioning_id", it is automatically added. Defaults to {}.
            blok_id (str, optional): Blok id, ex: `456a06cb008a2f6d72f04e94d26242d4607e80d5cf8d9a5aa34ec109117071c6`. Defaults to None.
            authorize (bool, optional): Put authorization headers in the request. Defaults to True.
            language (str, optional): Language of the response, ex: `fr`. Defaults to None.
            ignore_headers (set[str], optional): Ignore headers having the key in the set. Defaults to None.
            manual_headers (dict, optional): Add the dict to the final headers. Defaults to None.
            **kwargs: Arguments that will be passed to the `AsyncClient(...).request` method.

        Returns:
            InstagramResponse
        """
        return await self._request(
            **self.bloks_kwargs(
                app=app,
                payload=payload,
                blok_id=blok_id,
                authorize=authorize,
                language=language,
                ignore_headers=ignore_headers,
                manual_headers=manual_headers,
            ),
            **kwargs
        )