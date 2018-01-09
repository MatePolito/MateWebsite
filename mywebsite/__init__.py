from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
# this is the login view users will be redirected to if they are not logged in and they try to access a private page
login_manager.login_view = 'index'
#Configuration of Flask-Mail for gmail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'julientriquet69@gmail.com'
app.config['MAIL_PASSWORD'] = 'postbac69'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#Instance of mail
mail= Mail(app)


import views

