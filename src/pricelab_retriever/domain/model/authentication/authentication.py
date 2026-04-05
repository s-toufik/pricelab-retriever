import enum
from dataclasses import dataclass

class AuthType(enum.Enum):
    token = "__token__"
    basic = "__basic__"
    none = "__none__"

@dataclass(frozen=True, slots=True)
class Auth:
    type: AuthType

@dataclass(frozen=True, slots=True)
class TokenAuth(Auth):
    key_name: str
    key_value: str

@dataclass(frozen=True, slots=True)
class BasicAuth(Auth):
    username: str
    password: str