import dataclasses
from typing import List

import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass


@dataclass
class Cameras:
    cam_names: List[int] = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))
    cam_ids: List[int] = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))

    def dump(self):
        schema = desert.schema(Cameras)
        return schema.dump(self)
