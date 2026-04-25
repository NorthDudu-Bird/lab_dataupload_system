from marshmallow import EXCLUDE, Schema, fields, pre_load, validate


def _empty_to_none(data, *keys):
    for key in keys:
        if data.get(key) == "":
            data[key] = None
    return data


class UserCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(load_default="123456", validate=validate.Length(min=6, max=50))
    real_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.Str(load_default=None, allow_none=True)
    email = fields.Email(load_default=None, allow_none=True)
    role = fields.Str(required=True, validate=validate.OneOf(["admin", "reviewer", "reporter"]))
    status = fields.Str(load_default="enabled", validate=validate.OneOf(["enabled", "disabled"]))

    @pre_load
    def normalize_empty_values(self, data, **kwargs):
        return _empty_to_none(data, "phone", "email")


class UserUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    real_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.Str(load_default=None, allow_none=True)
    email = fields.Email(load_default=None, allow_none=True)
    role = fields.Str(required=True, validate=validate.OneOf(["admin", "reviewer", "reporter"]))
    status = fields.Str(required=True, validate=validate.OneOf(["enabled", "disabled"]))

    @pre_load
    def normalize_empty_values(self, data, **kwargs):
        return _empty_to_none(data, "phone", "email")


class UserStatusSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(["enabled", "disabled"]))


class ResetPasswordSchema(Schema):
    password = fields.Str(load_default="123456", validate=validate.Length(min=6, max=50))
