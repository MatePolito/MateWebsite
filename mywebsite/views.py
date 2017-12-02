from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from .forms import LoginUserForm, RegistrationForm, LoginMateForm
from .models import User

from . import app, db, login_manager

@login_manager.user_loader
def get_user(username):
    '''This is needed by LoginManager to retrieve a User instance based on its ID (in this case, username)'''
    return User.query.filter_by(username=username).first()

@app.before_first_request
def setup_db():
    db.create_all()

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/loginuser' , methods=['GET', 'POST'])
def loginuser():
    myForm = LoginUserForm()
    if myForm.validate_on_submit():
        # we are certain user exists because of the username validator of LoginForm
        user = get_user(myForm.username.data)
        if user.check_password(myForm.password.data):
            # login the user, then redirect to his user page
            login_user(user)
            flash('User logged in!', 'success')
            return redirect(url_for('user'))
        else:
            flash('Incorrect password!', 'danger')
    return render_template('loginuser.html', form=myForm)

@app.route('/loginmate', methods=['GET', 'POST'])
def loginmate():
    myForm = LoginMateForm()
    if myForm.validate_on_submit():
        # we are certain user exists because of the username validator of LoginForm
        user = get_user(myForm.username.data)
        if user.check_password(myForm.password.data):
            # login the user, then redirect to his user page
            login_user(user)
            flash('Mate logged in!', 'success')
            return redirect(url_for('mate'))
        else:
            flash('Incorrect password!', 'danger')

    return render_template('loginmate.html', form=myForm)

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/user')
@login_required
def user():
    '''You need to be logged in to access this page'''
    return render_template('user_profile.html')

@app.route('/mate')
@login_required
def mate():
    '''You need to be logged in to access this page'''
    return render_template('mate_profile.html')

@app.route('/listservice')
@login_required
def listservice():
    '''You need to be logged in to access this page'''
    return render_template('liste_service.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    phone_number=form.phone_number.data,
                    mail=form.mail.data,
                    address=form.address.data,
                    birthdate=form.birthdate.data

                    )
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('User succesfully registered', 'success')
        return redirect(url_for('loginuser'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User logged out!', 'success')
    return render_template('homepage.html')

@app.route('/modifyinformation', methods=['GET', 'POST'])
@login_required
def modifyinformation():
    form = RegistrationForm()
    if form.validate_on_submit():
        current_user.last_name = form.last_name.data

        db.session.add(user)
        flash('Your profile has been updated.')
        return redirect(url_for('user', username=current_user.username))
    form.last_name.data = current_user.last_name
    return render_template('modify_information.html', form=form)
