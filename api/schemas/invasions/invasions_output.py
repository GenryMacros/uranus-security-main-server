
import dataclasses

import desert
from marshmallow import fields, Schema
from marshmallow_dataclass import dataclass


@dataclass
class InvasionSchema:
    id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))

    def dump(self):
        schema = desert.schema(InvasionSchema)
        return schema.dump(self)


class InvasionData(Schema):
    id = fields.Integer(
            required=True,
            default=None
    )
    date = fields.Integer(
        required=True,
        default=None
    )
    link = fields.String(
        required=True,
        default=None
    )
    link_short = fields.String(
        required=True,
        default=None
    )


class GetInvasionsOutput(Schema):
    invasions = fields.List(fields.Nested(InvasionData))
