import desert
import dataclasses
from typing import List

from marshmallow import fields
from marshmallow_dataclass import dataclass


class CamInfo:
    def __init__(self, local_name: int, back_id: int, is_online: bool):
        self.local_name = local_name
        self.back_id = back_id
        self.is_online = is_online


@dataclass
class Cameras:
    cam_names: List[int] = dataclasses.field(metadata=desert.metadata(
        fields.List(
            fields.Integer,
            required=False
        )
    ))
    cam_ids: List[int] = dataclasses.field(metadata=desert.metadata(
        fields.List(
            fields.Integer,
            required=False
        )
    ))
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.Boolean(
            required=False
        )
    ))
    reason: str = fields.String(
                        required=False,
                        default=''
                    )

    def dump(self):
        schema = desert.schema(Cameras)
        return schema.dump(self)

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(Cameras)
        loaded_data: Cameras = schema.load(json_data, partial=True)
        return loaded_data


@dataclass
class DefaultResponse:
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.Boolean(
            required=False
        )
    ))
    reason: str = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=False
        )
    ))

    @classmethod
    def load(cls, json_data):
        schema = desert.schema(DefaultResponse)
        loaded_data: DefaultResponse = schema.load(json_data)
        return loaded_data
