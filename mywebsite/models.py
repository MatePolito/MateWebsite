from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date, datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    mail = db.Column(db.String)
    address = db.Column(db.String)
    birthdate= db.Column(db.Date)


    username = db.Column(db.String, nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.username


    @property
    def password(self):
        raise StandardError('Password is write-only')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Mate(db.Model, UserMixin):
    __tablename__ = 'mates'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    mail = db.Column(db.String)
    address = db.Column(db.String)
    birthdate = db.Column(db.Date)

    username = db.Column(db.String, nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.username

    @property
    def password(self):
        raise StandardError('Password is write-only')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Service(db.Model, UserMixin):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    typeservice = db.Column(db.String)
    description = db.Column(db.String)
    servicedate = db.Column(db.Date)

    def get_id(self):
        return self.username