from marshmallow import EXCLUDE, Schema, fields, validate


class LabSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    lab_code = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    lab_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    building = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    room_no = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    manager_name = fields.Str(load_default=None, allow_none=True)
    capacity = fields.Int(load_default=0, validate=validate.Range(min=0))
    status = fields.Str(load_default="enabled", validate=validate.OneOf(["enabled", "disabled"]))
    remark = fields.Str(load_default=None, allow_none=True)

