from marshmallow import EXCLUDE, Schema, fields, validate


class NoticeSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    content = fields.Str(required=True, validate=validate.Length(min=2))
    status = fields.Str(load_default="published", validate=validate.OneOf(["draft", "published"]))

