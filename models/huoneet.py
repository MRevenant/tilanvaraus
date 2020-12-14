from extensions import db


class Huoneet(db.Model):

    __tablename__ = 'huoneet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(),
                           onupdate=db.func.now())

    @classmethod
    def get_all_huoneet(cls):
        return cls.query.all()

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
