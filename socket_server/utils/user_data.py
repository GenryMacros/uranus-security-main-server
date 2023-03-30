import dataclasses
import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass


@dataclass
class UserData:
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
        schema = desert.schema(UserData)
        loaded_data: UserData = schema.load(json_data)
        if loaded_data.refreshToken is None or \
           loaded_data.userId is None or \
           loaded_data.token is None or \
           loaded_data.publicKey is None:
            raise ValueError("Received unacceptable auth data")
        return loaded_data

    def is_authenticated(self) -> bool:
        return self.token is not None
