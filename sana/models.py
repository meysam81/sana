from sana import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    pno = db.Column(db.String(20), unique = True, nullable = False)
    firstname = db.Column(db.String(50), nullable = True)
    lastname = db.Column(db.String(50), nullable = True)
    hashed_password = db.Column(db.String, nullable = True)

    def __init__(self, pno):
        self.pno = pno

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    @staticmethod
    def get_by_pno(pno):
        return User.query.filter_by(pno = pno).first()

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return '<User: {}>'.format(self.pno)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    request_addr = db.Column(db.String(30), unique = True)
    attempts = db.Column(db.Integer, default = 1)
    banned_until = db.Column(db.DateTime, nullable = True)

    def __repr__(self):
        return "{}: {}".format(self.request_addr, self.attempts)
