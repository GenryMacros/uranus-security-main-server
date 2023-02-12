import dataclasses
import re

import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass

from api.exceptions.clients.exceptions import EmailWrongFormat


@dataclass
class ClientCredentials:

    login: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    password: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(ClientCredentials)
        loaded_credentials: ClientCredentials = schema.load(json_data)
        if len(loaded_credentials.login) < 5 or len(loaded_credentials.login) >= 20:
            raise ValueError("Login or password is invalid")
        elif len(loaded_credentials.password) < 10 or len(loaded_credentials.password) >= 20:
            raise ValueError("Login or password is invalid")
        return loaded_credentials

    @classmethod
    def dump(cls, data):
        schema = desert.schema(ClientCredentials)
        return schema.dump(data)


@dataclass
class ClientSignup:
    username: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    password: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    email: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(ClientSignup)
        loaded_credentials: ClientSignup = schema.load(json_data)
        email_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

        if len(loaded_credentials.username) < 5 or len(loaded_credentials.username) >= 20:
            raise ValueError("Login or password is invalid")
        elif len(loaded_credentials.password) < 10 or len(loaded_credentials.password) >= 20:
            raise ValueError("Login or password is invalid")
        elif not re.fullmatch(email_regex, loaded_credentials.email):
            raise EmailWrongFormat()
        return loaded_credentials

    @classmethod
    def dump(cls, data):
        schema = desert.schema(ClientSignup)
        return schema.dump(data)


@dataclass
class ClientConfirmation:
    token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(ClientConfirmation)
        loaded_confirmation: ClientConfirmation = schema.load(json_data)
        return loaded_confirmation

    @classmethod
    def dump(cls, data):
        schema = desert.schema(ClientConfirmation)
        return schema.dump(data)


@dataclass
class ClientTokenRefresh:
    user_id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    jwt: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    refresh: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(ClientTokenRefresh)
        loaded_refresh: ClientTokenRefresh = schema.load(json_data)
        return loaded_refresh

    @classmethod
    def dump(cls, data):
        schema = desert.schema(ClientTokenRefresh)
        return schema.dump(data)
