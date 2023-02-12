from marshmallow_dataclass import dataclass


@dataclass
class JwtBody:
    id: int
    email: str
    expiration_date: int


@dataclass
class RefreshBody:
    id: int
    expiration_date: int


@dataclass
class JwtHeader:
    alg: str = "HS256"
    typ: str = "JWT"
