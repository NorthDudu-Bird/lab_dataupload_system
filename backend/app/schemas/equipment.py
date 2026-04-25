from marshmallow import EXCLUDE, Schema, fields, pre_load, validate


class EquipmentSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    equipment_code = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    equipment_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    brand = fields.Str(load_default=None, allow_none=True)
    model = fields.Str(load_default=None, allow_none=True)
    lab_id = fields.Int(required=True, validate=validate.Range(min=1))
    purchase_date = fields.Date(load_default=None, allow_none=True)
    status = fields.Str(
        load_default="normal",
        validate=validate.OneOf(["normal", "faulty", "maintenance", "scrapped"]),
    )
    remark = fields.Str(load_default=None, allow_none=True)

    @pre_load
    def normalize_empty_values(self, data, **kwargs):
        for key in ["brand", "model", "purchase_date", "remark"]:
            if data.get(key) == "":
                data[key] = None
        return data
