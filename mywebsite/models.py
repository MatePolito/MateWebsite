from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date, datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'))

                         )
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    mail = db.Column(db.String)
    address = db.Column(db.String)
    birthdate= db.Column(db.Date)
    roleuser_id= db.Column(db.Integer, db.ForeignKey('roles.id'))
    roleuser = relationship("Role")

    '''services = db.relationship('Service', backref='role', lazy='dynamic')

    servicesmate = db.relationship('Service', backref='users')'''



    servicerequest = db.relationship('Service',
                              secondary=registrations,
                              backref=db.backref('users', lazy='dynamic'),
                              lazy='dynamic')


    username = db.Column(db.String, nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

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
    servicetype = db.Column(db.String)
    servicename = db.Column(db.String)
    servicedescription = db.Column(db.String)
    servicedate = db.Column(db.Date)
    servicecity=db.Column(db.String)
    servicestate = db.Column(db.Integer)

    userrank = db.Column(db.Integer)
    userfeedback = db.Column(db.String)

    materank=db.Column(db.Integer)
    matefeedback = db.Column(db.String)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=[user_id])

    mate_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mate = relationship("User", foreign_keys=[mate_id])

    def get_id(self):
        return self.username





class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')




class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


