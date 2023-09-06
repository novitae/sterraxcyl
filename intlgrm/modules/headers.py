from typing import Literal, Self
from xeger import xeger
import random
import re

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