import dataclasses

import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass


@dataclass
class LoginResponse:
    id: int = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    public_key: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    auth_token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    refresh_token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(LoginResponse)
        loaded_response: LoginResponse = schema.load(json_data)
        return loaded_response

    @classmethod
    def dump(cls, data):
        schema = desert.schema(LoginResponse)
        return schema.dump(data)


@dataclass
class ClientConfirmationResponse:
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))


@dataclass
class ClientSecretSchema:
    password_hash: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    password_salt: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    user_private: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    user_public: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))


@dataclass
class ClientContactSchema:
    email: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    phone: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    telegram: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(ClientContactSchema)
        loaded_response: ClientContactSchema = schema.load(json_data)
        return loaded_response

    @classmethod
    def dump(cls, data):
        schema = desert.schema(ClientContactSchema)
        return schema.dump(data)


@dataclass
class ClientLocationSchema:
    country: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    city: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    addr: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    ind: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(ClientLocationSchema)
        loaded_response: ClientLocationSchema = schema.load(json_data)
        return loaded_response

    @classmethod
    def dump(cls, data):
        schema = desert.schema(ClientLocationSchema)
        return schema.dump(data)
