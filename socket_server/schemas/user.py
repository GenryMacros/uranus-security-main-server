import dataclasses

import desert
from marshmallow import fields, Schema
from marshmallow_dataclass import dataclass


@dataclass
class UserAuthData:
    publicKey: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True,
            default=None
        )
    ))
    token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True,
            default=None
        )
    ))
    refreshToken: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True,
            default=None
        )
    ))
    userId: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True,
            default=None
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(UserAuthData)
        loaded_data: UserAuthData = schema.load(json_data)
        if loaded_data.refreshToken is None or \
           loaded_data.userId is None or \
           loaded_data.token is None or \
           loaded_data.publicKey is None:
            raise ValueError("Received unacceptable auth schemas")
        return loaded_data

    def is_authenticated(self) -> bool:
        return self.token is not None


class CamData(Schema):
    cam_name = fields.Integer(
            required=True,
            default=None
        )

    cam_id = fields.Integer(
            required=True,
            default=None
        )

    is_online = fields.Boolean(
            required=True,
            default=False
        )


class GetCamerasResponse(Schema):
    cameras = fields.List(fields.Nested(CamData))
    success = fields.Boolean()


@dataclass
class AuthenticateResponse:
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.Boolean(
            required=True,
            default=False
        )
    ))

    def dump(self):
        schema = desert.schema(AuthenticateResponse)
        return schema.dump(self)
