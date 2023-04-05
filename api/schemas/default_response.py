import dataclasses

import desert
from marshmallow import fields
from marshmallow_dataclass import dataclass


@dataclass
class DefaultResponse:
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.Boolean(
            default=True
        )
    ))

    def dump(self):
        schema = desert.schema(DefaultResponse)
        return schema.dump(self)
