from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

from schemas.user import UserSchema


class HuoneetSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dumb_only=True)
    name = fields.String(required=True,)
    updated_at = fields.DateTime(dumb_only=True)

    author = fields.Nested(UserSchema, attribute='user', dumb_only=True,
                           only=['id', 'username'])
