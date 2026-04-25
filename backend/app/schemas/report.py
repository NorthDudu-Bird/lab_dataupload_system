from marshmallow import EXCLUDE, Schema, fields, validate


class ReportSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    report_date = fields.Date(required=True)
    lab_id = fields.Int(required=True, validate=validate.Range(min=1))
    temperature = fields.Decimal(required=True, as_string=False, places=2)
    humidity = fields.Decimal(required=True, as_string=False, places=2)
    hygiene_status = fields.Str(required=True, validate=validate.OneOf(["normal", "abnormal"]))
    power_status = fields.Str(required=True, validate=validate.OneOf(["normal", "abnormal"]))
    network_status = fields.Str(required=True, validate=validate.OneOf(["normal", "abnormal"]))
    door_window_status = fields.Str(required=True, validate=validate.OneOf(["normal", "abnormal"]))
    fire_status = fields.Str(required=True, validate=validate.OneOf(["normal", "abnormal"]))
    equipment_status = fields.Str(required=True, validate=validate.OneOf(["normal", "abnormal"]))
    usage_count = fields.Int(required=True, validate=validate.Range(min=0))
    abnormal_desc = fields.Str(load_default=None, allow_none=True)
    attachment_path = fields.Str(load_default=None, allow_none=True)


class ReviewSchema(Schema):
    review_status = fields.Str(required=True, validate=validate.OneOf(["approved", "rejected"]))
    review_comment = fields.Str(required=True, validate=validate.Length(min=1, max=500))

