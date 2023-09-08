from typing import Literal, Self
from xeger import xeger
import random
import re

from .. import utils
from . import bloks, authorization

version_generation_map = (
    (210, 299), # <-- for bloks, otherwise --> (162, 260),
    (0, 9),
    (0, 9),
    (10, 99),
    (100, 999)
)

def random_tuple_version() -> tuple[int]:
    return tuple([random.randint(*ranges) for ranges in version_generation_map])

def random_str_version() -> str:
    return ".".join(random_tuple_version())

def random_app_id() -> int:
    return int(xeger(r"[1-9]\d{14}"))

class DeviceLanguage:
    def __init__(
        self,
        language: Literal["fr", "en"] = "en",
        country: Literal["fr", "us"] = "us",
    ) -> None:
        self.language = language
        self.country = country

    @property
    def both(self) -> str:
        return f"{self.language}-{self.country.upper()}"
    
    def to_dict(self) -> dict:
        return {
            "language": self.language,
            "country": self.country,
        }

    def to_headers(self) -> dict:
        country = self.country.upper()
        return {
            "X-IG-App-Startup-Country": country,
            "X-IG-Device-Locale": self.both,
            "X-IG-App-Locale": self.language,
            "X-IG-Mapped-Locale": self.both.replace("-", "_"),
            "Accept-Language": self.both
        }
    
class Device:
    def __init__(
        self,
        device: str,
        version: tuple[int],
        locale: str,
        language: str,
        scale: float,
        resolution: tuple[int],
        platform_id: int,
    ) -> None:
        self.device = device
        self.version = version
        self.locale = locale
        self.language = language
        self.scale = scale
        self.resolution = resolution
        self.platform_id = platform_id

    def __repr__(self) -> str:
        return f"Device({self.device} {self.version}, scale: {self.scale}, res: {self.resolution})"

    def __str__(self) -> str:
        return self.to_raw()

    def to_raw(self) -> str:
        return "(" + "; ".join([ self.device,
                                 f"iOS " + "_".join(map(str, self.version)),
                                 self.locale,
                                 self.language,
                                 f"scale={self.scale:.2f}",
                                 "x".join(map(str, self.resolution)),
                                 str(self.platform_id) ]) + ")"

    @classmethod
    def from_raw(
        cls,
        string: str,
    ) -> Self:
        assert isinstance(string, str)
        device, version, locale, language, scale, resolution, platform_id = string.strip("()").split("; ")
        return cls(
            device=device,
            version=tuple(int, version.split(" ", 1)[-1].split("_")),
            locale=locale,
            language=language,
            scale=float(scale.split("=", 1)[1]),
            resolution=tuple(map(int, resolution.split("x"))),
            platform_id=int(platform_id),
        )
    
    @classmethod
    def from_random(
        cls,
        lg: DeviceLanguage = None
    ) -> Self:
        return cls(
            device="iPhone7,2",
            version=(12, 5, 5),                 # à random
            locale=lg.both,
            language=lg.both.replace("-", "_"),
            scale=2.0,                          # à random
            resolution=(9999, 9999),            # à random
            platform_id=432065435
        )
    
    def overwrite_language(
        self,
        lg: DeviceLanguage
    ) -> None:
        self.language = lg.language
        self.locale = lg.country

user_agent_parse = re.compile(r"(?P<name>\w+) (?P<version>\d+(?:\.\d+)+) (?P<device>\(.+\)) (?P<webkit>.+)")

class UserAgent:
    def __init__(
        self,
        name: str,
        version: tuple[int],
        device: Device,
        webkit: str = None
    ) -> None:
        self.name = name
        self.version = version
        self.device = device
        self.webkit = webkit or "AppleWebKit/420+"

    def __repr__(self) -> str:
        return f"UserAgent({self.name} {self.version}, {self.device})"
    
    def __str__(self) -> str:
        return self.to_raw()

    def to_raw(self) -> str:
        return " ".join([
            self.name,
            ".".join(map(str, self.version)),
            str(self.device),
            self.webkit,
        ])

    @classmethod
    def from_raw(
        cls,
        string: str
    ) -> Self:
        assert isinstance(string, str)
        if match := user_agent_parse.search(string):
            data = match.groupdict()
            return cls(
                name=data.pop("name"),
                version=tuple(map(int, data.pop("version").split("."))),
                device=Device.from_raw(data.pop("device")),
                webkit=data.pop("webkit"),
            )
        else:
            raise ValueError("Invalid useragent format")

    @classmethod
    def from_random(
        cls,
        device: Device = None,
        lg: DeviceLanguage = None,
    ) -> Self:
        return cls(
            name="Instagram",
            version=random_tuple_version(),
            device=device or Device.from_random(lg=lg)
        )
    
    def overwrite_language(
        self,
        lg: DeviceLanguage
    ) -> None:
        self.device.overwrite_language(lg)

def random_request_analytics(
    product: str = "igios",
    request_category: str = "api"
) -> str:
    """Makes a random request analytics for facebook"""
    return utils.flat_json_dumps({
        "network_tags": {
            "product": product,
            "purpose": "fetch",
            "request_category": request_category,
            "retry_attempt": "0"
        }
    })

class DeviceStats:
    """
        Stats about the devide that makes it more credible for the server
        recieving the requests.
    """
    def __init__(
        self,
        connection_speed: int = None,
        connection_type: Literal['WiFi'] = None,
        timezone_offset: int = None,
        ig_capabilites: Literal["36r/F/8="] = None,
        abr_connection_speed: int = None,
        client_endpoint: Literal[""] = None,
        bandwidth_speed: float = None,
        app_id: int = None,
        nav_chain: Literal["not_init"] = None,
        request_analystics: Literal["recvTime=0;reqTime=0;tkn=;tts=0;ip=;v=;fail=NoUrlMap;cached=0"] = None,
        bkid: bytes = None,
    ) -> None:
        self.connection_speed = connection_speed or -1
        self.connection_type = connection_type or "WiFi"
        self.timezone_offset = timezone_offset or 3600
        self.ig_capabilites = ig_capabilites or "36r/F/8="
        self.abr_connection_speed = abr_connection_speed or 0
        self.client_endpoint = client_endpoint or ""
        self.bandwidth_speed = bandwidth_speed or 0.0
        self.app_id = app_id or random_app_id()
        self.nav_chain = nav_chain or "not_init"
        self.bkid = bkid or bloks.bkid.DEFAULT_BKID
        self.request_analystics = request_analystics or random_request_analytics()

    def to_headers(self) -> dict:
        return {
            "X-IG-Connection-Speed": f"{self.connection_speed}kbps",
            "X-IG-Connection-Type": self.connection_type,
            "X-IG-Timezone-Offset": self.timezone_offset,
            "X-IG-Capabilities": self.ig_capabilites,
            "X-IG-ABR-Connection-Speed-KBPS": self.abr_connection_speed,
            "X-IG-CLIENT-ENDPOINT": self.client_endpoint,
            "X-IG-Bandwidth-Speed-KBPS": f"{self.bandwidth_speed:.3f}",
            "X-IG-App-ID": self.app_id,
            "X-IG-Nav-Chain": self.nav_chain,
            "X-FB-Connection-Type": self.connection_type.lower(),
            "X-FB-HTTP-Engine": "Liger",
            "X-FB-Client-IP": True,
            "X-FB-Server-Cluster": True,
            "x-fb-rmd": "recvTime=0;reqTime=0;tkn=;tts=0;ip=;v=;fail=NoUrlMap;cached=0",
            "X-FB-Friendly-Name": "api",
            "X-FB-Request-Analytics-Tags": self.request_analystics,
            "X-Bloks-Version-Id": self.bkid,
            "X-Tigon-Is-Retry": False,
            "Priority": "u=2, i"
        }
    
    def to_dict(self) -> dict:
        return {
            "connection_speed": self.connection_speed,
            "connection_type": self.connection_type,
            "timezone_offset": self.timezone_offset,
            "ig_capabilites": self.ig_capabilites,
            "abr_connection_speed": self.abr_connection_speed,
            "client_endpoint": self.client_endpoint,
            "bandwidth_speed": self.bandwidth_speed,
            "app_id": self.app_id,
            "nav_chain": self.nav_chain,
            "bkid": self.bkid,
            "request_analystics": self.request_analystics
        }
    
    # accept_encoding: str = Field("gzip, deflate", alias="Accept-Encoding")

    def change_app_id(
        self,
        new_app_id: int = None
    ) -> None:
        self.x_ig_app_id = new_app_id or random_app_id()

class DeviceID:
    def __init__(
        self,
        device_id: str = None,
        pigeon_session_id: str = None,
    ) -> None:
        self.device_id = device_id
        self.pigeon_session_id = pigeon_session_id

    def __repr__(self) -> str:
        return f"DeviceID(device: {self.device_id}, pigeon: {self.pigeon_session_id})"
    
    def to_headers(self) -> dict:
        return {
            "X-IG-Device-ID": self.device_id,
            "X-IG-Family-Device-ID": self.device_id,
            "X-Pigeon-Session-Id": self.pigeon_session_id,
        }
    
    def to_dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "pigeon_session_id": self.pigeon_session_id,
        }
    
class DynamicHeaders:
    def __init__(
        self,
        www_claim: str = None,
        x_mid: str = None,
        ig_u_ig_direct_region_hint: str = None,
        ig_u_shbid: str = None,
        ig_u_shbts: str = None,
        ig_u_rur: str = None,
        ig_u_ds_user_id: str = None,
    ) -> None:
        self.www_claim = www_claim
        self.x_mid = x_mid
        self.ig_u_ig_direct_region_hint = ig_u_ig_direct_region_hint
        self.ig_u_shbid = ig_u_shbid
        self.ig_u_shbts = ig_u_shbts
        self.ig_u_rur = ig_u_rur
        self.ig_u_ds_user_id = ig_u_ds_user_id

    def update(
        self,
        headers: dict[str, str]
    ) -> None:
        if www_claim := headers.get("x-ig-set-www-claim"):
            self.www_claim = www_claim
        if x_mid := headers.get("ig-set-x-mid"):
            self.x_mid = x_mid
        if ig_u_ig_direct_region_hint := headers.get("ig-set-ig-u-ig-direct-region-hint"):
            self.ig_u_ig_direct_region_hint = ig_u_ig_direct_region_hint
        if ig_u_shbid := headers.get("ig-set-ig-u-shbid"):
            self.ig_u_shbid = ig_u_shbid
        if ig_u_shbts := headers.get("ig-set-ig-u-shbts"):
            self.ig_u_shbts = ig_u_shbts
        if ig_u_rur := headers.get("ig-set-ig-u-rur"):
            self.ig_u_rur = ig_u_rur
        if ig_u_ds_user_id := headers.get("ig-set-ig-u-ds-user-id"):
            self.ig_u_ds_user_id = ig_u_ds_user_id

    def to_headers(self) -> dict:
        return {
            key: value for key, value in [
                ("X-IG-WWW-Claim", self.www_claim),
                ("X-MID", self.x_mid),
                ("IG-U-IG-Direct-Region-Hint", self.ig_u_ig_direct_region_hint),
                ("IG-U-Shbid", self.ig_u_shbid),
                ("IG-U-Shbts", self.ig_u_shbts),
                ("IG-U-Rur", self.ig_u_rur),
                ("IG-U-Ds-User-ID", self.ig_u_ds_user_id),
            ] if value is not None
        }
    
    def to_dict(self) -> dict:
        return {
            "www_claim": self.www_claim,
            "x_mid": self.x_mid,
            "ig_u_ig_direct_region_hint": self.ig_u_ig_direct_region_hint,
            "ig_u_shbid": self.ig_u_shbid,
            "ig_u_shbts": self.ig_u_shbts,
            "ig_u_rur": self.ig_u_rur,
            "ig_u_ds_user_id": self.ig_u_ds_user_id,
        }
    
class Headers:
    def __init__(
        self,
        language: DeviceLanguage = None,
        user_agent: UserAgent = None,
        stats: DeviceStats = None,
        deviceid: DeviceID = None,
        dyn_headers: DynamicHeaders = None,
    ) -> None:
        self.language = language or DeviceLanguage("en", "us")
        self.user_agent = user_agent or UserAgent.from_random(lg=self.language)
        self.stats = stats or DeviceStats()
        self.deviceid = deviceid or DeviceID()
        self.dyn_headers = dyn_headers or DynamicHeaders()

    @staticmethod
    def content_type_from_body(
        has_body: bool = False,
        content_type: str = None
    ) -> dict:
        return {**({"Content-Type": content_type or "application/x-www-form-urlencoded; charset=UTF-8"} if has_body else {})}

    def to_headers(
        self,
        auth: authorization.Authorization = None,
        has_body: bool = False,
        content_type: str = None,
        ignore_headers: set[str] = None,
    ) -> dict:
        result = {
            **self.language.to_headers(),
            "User-Agent": str(self.user_agent),
            **(auth.to_headers() if auth else {}),
            **self.stats.to_headers(),
            **self.deviceid.to_headers(),
            **self.dyn_headers.to_headers(),
            **self.content_type_from_body(has_body, content_type)
        }
        if ignore_headers:
            return dict(filter(lambda items: items[0] in ignore_headers, result.items()))
        else:
            return result