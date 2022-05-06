from extensions import db


class Shortcut(db.Model):
    __tablename__ = 'shortuct'

    id = db.Column(db.Integer, primary_key=True)
    combination = db.Column(db.String(100), nullable=False)
    explanation = db.Column(db.String(1000), nullable=False)

    def __init__(self, id, combinantion, explanation):
        self.id = id
        self.combination = combinantion
        self.explanation = explanation

    def save(self):
        db.session.add(self)
        db.session.commit();
