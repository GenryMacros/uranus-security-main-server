import re

import desert
from marshmallow_dataclass import dataclass

from api.exceptions.clients.exceptions import EmailWrongFormat


@dataclass
class JwtBody:
    id: int
    email: str
    expiration_date: float

    def __init__(self, id: int, email: str, expiration_date: float):
        self.id = id
        self.email = email
        self.expiration_date = expiration_date

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(JwtBody)
        loaded_credentials: JwtBody = schema.load(json_data)
        email_regex = re.compile(
            r"^([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        if re.fullmatch(email_regex, loaded_credentials.email):
            raise EmailWrongFormat()
        return loaded_credentials

    @classmethod
    def dump(cls, data):
        schema = desert.schema(JwtBody)
        return schema.dump(data)


@dataclass
class RefreshBody:
    id: int
    expiration_date: float

    def __init__(self, id: int, expiration_date: float):
        self.id = id
        self.expiration_date = expiration_date

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(RefreshBody)
        refresh_response: RefreshBody = schema.load(json_data)
        return refresh_response

    @classmethod
    def dump(cls, data):
        schema = desert.schema(JwtBody)
        return schema.dump(data)


@dataclass
class JwtHeader:
    alg: str = "HS256"
    typ: str = "JWT"

    @classmethod
    def dump(cls, data):
        schema = desert.schema(JwtBody)
        return schema.dump(data)
