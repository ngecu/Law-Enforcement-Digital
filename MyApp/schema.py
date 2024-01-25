from marshmallow import Schema, fields

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    role = fields.Str(required=True)
    password = fields.Str(required=True)


class IncidentSchema(Schema):
    incident_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    accused = fields.Str(required=True)
    victim = fields.Str(required=True)
    reported_by = fields.Str(required=True)
    location = fields.Str(required=True)
    date = fields.Str(required=True)
    message = fields.Str(required=True)
    status = fields.Str(required=True)
