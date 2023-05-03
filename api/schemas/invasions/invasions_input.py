
import dataclasses
from typing import List

import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass


@dataclass
class InvasionAdd:
    auth_token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    path: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    cam_id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    client_id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    invaders: List[str] = dataclasses.field(metadata=desert.metadata(
        fields.List(
            fields.String,
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(InvasionAdd)
        loaded_response: InvasionAdd = schema.load(json_data)
        return loaded_response

    def dump(self):
        schema = desert.schema(InvasionAdd)
        return schema.dump(self)


@dataclass
class InvasionGet:
    auth_token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    cam_id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    client_id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    date: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
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
        schema = desert.schema(InvasionGet)
        loaded_response: InvasionGet = schema.load(json_data)
        return loaded_response

    def dump(self):
        schema = desert.schema(InvasionGet)
        return schema.dump(self)


@dataclass
class InvasionDelete:
    auth_token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    invasion_id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    client_id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(InvasionDelete)
        loaded_response: InvasionDelete = schema.load(json_data)
        return loaded_response

    def dump(self):
        schema = desert.schema(InvasionDelete)
        return schema.dump(self)
