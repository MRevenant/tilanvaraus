from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


class VarausSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    tila = fields.String(required=True, validate=[validate.Length(max=10)])
    paiva = fields.String(validate=[validate.Length(max=10)])
    aika = fields.Integer()
    henkiloita = fields.Integer()
    kuka = fields.String(validate=[validate.Length(max=50)])
    sahkoposti = fields.String(validate=[validate.Length(max=50)])

    author = fields.Nested(UserSchema, attribute='user', dump_only=True,
                           only=['id', 'username'])

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

    @validates('henkiloita')
    def validate_henkiloita(self, value):
        if value > 10:
            raise ValidationError('Because of Corona,. there cant be more than 10 people in a room')
        if value < 1:
            raise ValidationError('Cant be 0')

    @validates('aika')
    def validate_aika(self, value):
        if value > 2100:
            raise ValidationError('School is closed.')
        if value < 1400:
            raise ValidationError('Cant reserve spaces yet.')
