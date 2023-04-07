import dataclasses
from typing import List

import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass


@dataclass
class Cameras:
    cam_names: List[int] = dataclasses.field(metadata=desert.metadata(
        fields.List(
            fields.Integer,
            required=True
        )
    ))
    cam_ids: List[int] = dataclasses.field(metadata=desert.metadata(
        fields.List(
            fields.Integer,
            required=True
        )
    ))
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.Boolean(
            required=False
        )
    ))

    def dump(self):
        schema = desert.schema(Cameras)
        return schema.dump(self)
