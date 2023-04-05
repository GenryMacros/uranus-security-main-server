from typing import List

from marshmallow import fields, Schema
import dataclasses

import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass


class CamData(Schema):
    cam_id = fields.Integer(
            required=True,
            default=None
        )


class CamsRegister(Schema):
    id: int = fields.List(fields.Integer)
    auth_token: str = fields.List(fields.String)
    cameras = fields.List(fields.Nested(CamData))


@dataclass
class CamsGet:
    id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    auth_token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(CamsGet)
        loaded_response: CamsGet = schema.load(json_data)
        return loaded_response

    def dump(self):
        schema = desert.schema(CamsGet)
        return schema.dump(self)


@dataclass
class CamsDelete:
    id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    auth_token: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    cam_names: List[int] = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(CamsGet)
        loaded_response: CamsGet = schema.load(json_data)
        return loaded_response

    def dump(self):
        schema = desert.schema(CamsGet)
        return schema.dump(self)
