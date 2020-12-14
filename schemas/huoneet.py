from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

from schemas.user import UserSchema


class HuoneetSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dumb_only=True)
    name = fields.String(required=True, validate=[validate.length(max=100)])
    updated_at = fields.DateTime(dumb_only=True)

    @post_dumb(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

    author = fields.Nested(UserSchema, attribute='user', dumb_only=True,
                           only=['id', 'username'])
