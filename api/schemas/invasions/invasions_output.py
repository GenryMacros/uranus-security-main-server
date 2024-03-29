
import dataclasses

import desert
from marshmallow import fields, Schema
from marshmallow_dataclass import dataclass


@dataclass
class GetStatisticOutput:
    latest: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    intruders: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    duration: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    invasions: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.String(
            required=True
        )
    ))

    def dump(self):
        schema = desert.schema(GetStatisticOutput)
        return schema.dump(self)


@dataclass
class InvasionSchema:
    id: int = dataclasses.field(metadata=desert.metadata(
        fields.Integer(
            required=True
        )
    ))
    success: bool = dataclasses.field(metadata=desert.metadata(
        fields.String(
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
    file_name = fields.String(
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
    invaders = fields.List(
        fields.String
    )


class GetInvasionsOutput(Schema):
    invasions = fields.List(fields.Nested(InvasionData))
    success = fields.Boolean(
        required=True,
        default=False
    )
    reason = fields.String(
        required=False
    )
