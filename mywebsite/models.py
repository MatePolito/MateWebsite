from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date, datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'))

                         )
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    """ ATTRIBUTES"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    mail = db.Column(db.String)
    address = db.Column(db.String)
    birthdate= db.Column(db.Date)

    servicerequest = db.relationship('Service',
                                     secondary=registrations,
                                     backref=db.backref('users', lazy='dynamic'),
                                     lazy='dynamic')

    """ FOIREIGN KEYS"""

    roleuser_id= db.Column(db.Integer, db.ForeignKey('roles.id'))
    roleuser = relationship("Role")

    """ LOG-IN ATTRIBUTES """

    username = db.Column(db.String, nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String, nullable=False)
    
    #Token generation and verification
    confirmed = db.Column(db.Boolean, default=False)

    """ Function"""

    #Generation of a token with a default validity of one hour
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    '''Verification of the token: return true if the signature is okay, the expiration time isn't passed 
    and the id from the token and the user logged in match'''
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            #Verification the signature and the expiration time
            data = s.loads(token)
        except:
            return False
            #Check the match between the id from the token and the user logged in
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

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


class Service(db.Model):
    __tablename__ = 'services'

    """ ATTRIBUTES"""

    id = db.Column(db.Integer, primary_key=True)
    servicetype = db.Column(db.String)
    servicename = db.Column(db.String)
    servicedescription = db.Column(db.String)
    servicedate = db.Column(db.Date)
    servicecity=db.Column(db.String)
    servicestate = db.Column(db.Integer)
    servicebeg=db.Column(db.DateTime)
    servicetime = db.Column(db.Integer)

    userrank = db.Column(db.Integer)
    userfeedback = db.Column(db.String)

    materank=db.Column(db.Integer)
    matefeedback = db.Column(db.String)

    """ FOIREIGN KEYS"""

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=[user_id])

    mate_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mate = relationship("User", foreign_keys=[mate_id])



class Role(db.Model):
    __tablename__ = 'roles'

    """ ATTRIBUTES"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')




