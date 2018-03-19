from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField, TextAreaField, SelectField, DateTimeField, RadioField
from wtforms.validators import DataRequired, NumberRange, Length, EqualTo, ValidationError, Email
from .models import User
from flask import Flask, render_template
from flask_wtf import Form
from wtforms import DateField
from datetime import datetime
from wtforms import fields, widgets
from datetime import date

class NameForm(Form):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[NumberRange(min=18)])
    submit = SubmitField('Submit')



def number(form, field):
    for c in field.data:
        if  c < '0' and c > '9':
            raise ValidationError('Field must be numbers')
        if len(field.data)<10:
            raise ValidationError('Field must be at least 10 numbers long')

class RegistrationForm(Form):
    choice=RadioField('Label', choices=[('1', 'User'), ('2', 'Mate')])
    first_name = StringField('First name', validators=[DataRequired()], render_kw={"placeholder": "Carlo"})
    last_name = StringField('Last name', validators=[DataRequired()], render_kw={"placeholder": "D'Ambrosio"})
    username = StringField('Username', validators=[DataRequired(), Length(min=4)], render_kw={"placeholder": "Carlo1995"})
    phone_number = StringField('Phonenumber', validators=[DataRequired(), number], render_kw={"placeholder": "+39610101010"})
    mail = StringField('Mail', validators=[DataRequired(), Email(message=None)], render_kw={"placeholder": "carlo.dambrosio@gmail.com"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Torino"})
    birthdate=DateField('Birthdate', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD ('1995-11-19')"})

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists')



class ModifyInformationForm(Form):
    first_name = StringField('First name', render_kw={"placeholder": "Carlo"})
    last_name = StringField('Last name', render_kw={"placeholder": "D'Ambrosio"})
    birthdate = DateField('Birthdate', render_kw={"placeholder": "YYYY-MM-DD ('1995-11-19')"})
    address = StringField('Address', render_kw={"placeholder": "80, Via Giordano Bruno Torino"})
    phone_number = StringField('Phonenumber', validators=[number],render_kw={"placeholder": "+39610101010"})

    mail = StringField('Mail', render_kw={"placeholder": "carlo.dambrosio@gmail.com"})

    submit = SubmitField('Modify')


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

def datep(form, field):
        if  field.data<date.today():
            raise ValidationError("This date is passed! Enter a valid date")


class CreateServiceForm(Form):
    servicetype = SelectField('Type of Service', choices=[('ht', 'Home task'), ('st', 'Shopping task'), ('cf', 'Car fare')])
    servicename = StringField("Name of the service", validators=[DataRequired()], render_kw={"placeholder": "Help in doing shopping task"})
    servicedescription = TextAreaField('Description du service')
    servicedate=DateField("Date of the service", validators=[DataRequired(),datep], render_kw={"placeholder": "YYYY-MM-DD ('1995-11-19')"})
    servicecity=StringField("City of the service", validators=[DataRequired()], render_kw={"placeholder": "Torino"})
    servicebeg=DateTimeField("Estimated Beginning (hour) ",format='%H:%M', validators=[DataRequired()], render_kw={"placeholder": "15:00"})
    servicetime=IntegerField("Estimated Time (hour) ", validators=[DataRequired()], render_kw={"placeholder": "1"})
    submit = SubmitField('Create Service')

class ResearchServiceForm(Form):
    servicetype = SelectField('Type of Service', choices=[('none', '- Type of Service -'),('ht', 'Home task'), ('st', 'Shopping task'), ('cf', 'Car fare')])
    servicename = StringField("Name of the service", validators=[DataRequired()])
    servicedescription = TextAreaField('Description du service')
    servicedate=DateField("Date of the service", validators=[DataRequired()])
    servicecity=StringField("City of the service", validators=[DataRequired()])
    submit = SubmitField('Create Service')

class FeedbackForm(Form):
    rank = IntegerField("Rank the service from 1 to 5", validators=[NumberRange(min=1), NumberRange(max=5) ], render_kw={"placeholder": "1 - 5"})
    com = TextAreaField('Description du service')

    submit = SubmitField('Give Feedback and close the service')