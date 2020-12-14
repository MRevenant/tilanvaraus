from extensions import db

varaus_list = []


def get_last_id():
    if varaus_list:
        last_varaus = varaus_list[-1]
    else:
        return 1
    return last_varaus.id + 1


class Varaus(db.Model):
    __tablename__ = 'varaus'

    id = db.Column(db.Integer(), primary_key=True)
    tila = db.Column(db.String(100), nullable=False)
    paiva = db.Column(db.Integer, nullable=False)
    aika = db.Column((db.String(5)), nullable=False)
    henkiloita = db.Column(db.Integer)
    kuka = db.Column((db.String(25)), nullable=False)
    sahkoposti = db.Column((db.String(50)), nullable=False)
    is_publish = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(),
                           onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
