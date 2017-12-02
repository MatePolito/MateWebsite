from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, NumberRange, Length, EqualTo, ValidationError
from .models import User
from flask import Flask, render_template
from flask_wtf import Form
from wtforms import DateField
from datetime import date

class NameForm(Form):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[NumberRange(min=18)])
    submit = SubmitField('Submit')



class RegistrationForm(Form):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists')


class LoginUserForm(Form):
    username = StringField('User name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login as User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('User name does not exist')

class LoginMateForm(Form):
    username = StringField('Mate name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login as Mate')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Mate name does not exist')