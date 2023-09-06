from typing import Self
import urllib.parse
import base64
import json

class Authorization:
    def __init__(
        self,
        user_id: int,
        security: str,
        nsession: int,
    ) -> None:
        self.user_id = user_id
        self.security = security
        self.nsession = nsession

    def __repr__(self) -> str:
        return f"Authorization(uid: {self.user_id}, nsession: {self.nsession})"
    
    def __hash__(self) -> int:
        return hash(repr(self))
    
    def to_dict(self) -> list[str]:
        return list(map(str, [self.user_id, self.security, self.nsession]))

    @classmethod
    def from_raw(
        cls,
        raw_auth: str | list[str] | dict[str, str]
    ) -> Self:
        if isinstance(raw_auth, str):
            if raw_auth.startswith(("Bearer ", "IGT:2:")):
                raw_auth = base64.b64decode(raw_auth.split(":")[-1].encode()).decode()
                raw_auth = json.loads(raw_auth)['sessionid']
            raw_auth = urllib.parse.unquote(raw_auth)
            assert raw_auth.count(":") >= 3
            raw_auth = raw_auth.split(":")
        elif isinstance(raw_auth, dict):
            raw_auth = list(raw_auth.values())
        if isinstance(raw_auth, list):
            assert (user_id := raw_auth.pop(0)).isdigit()
            assert len((security := raw_auth.pop(0))) == 14
            assert 0 <= (nsession := int(raw_auth.pop(0))) < 32
            return cls( user_id=int(user_id),
                        security=security,
                        nsession=nsession, )
        else:
            raise ValueError('the auth was not recognized')

class UserSession:
    def __init__(
        self
    ) -> None:
        pass

    @classmethod
    async def from_credentials(
        cls,
        username: str,
        password: str,
    ) -> Self:
        ""

    @classmethod
    def from_authorization(
        cls,
        authorization: Authorization
    ) -> Self:
        ""