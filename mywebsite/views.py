from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from .forms import LoginUserForm, RegistrationForm, LoginMateForm, ModifyInformationForm, CreateServiceForm, ResearchServiceForm
from .forms import LoginUserForm, RegistrationForm, LoginMateForm
from .models import User, Service, Role, Permission
from flask_login import current_user
from flask_mail import Mail, Message

from . import app, db, login_manager, mail


def notification():
    msg = Message('Hello', sender='julientriquet69@gmail.com', recipients=['julientriquet69@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"

app.config['FLASKY_MAIL_SENDER'] = 'julientriquet69@gmail.com'

def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template +'.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

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
            return redirect(url_for('user'))
        else:
            flash('Incorrect password!', 'danger')

    return render_template('loginmate.html', form=myForm)

@app.route('/servicepage', methods=['GET', 'POST'])
@app.route('/servicepage/<int:idservice>/<int:idserviceuser>', methods=['GET', 'POST'])
def servicepage(idservice, idserviceuser):
    '''print idserviceuser
    print idservice'''
    service = Service.query.filter_by(id=idservice).first()
    serviceuser= User.query.filter_by(id=idserviceuser).first()
    '''print serviceuser.username
    print service.servicename'''
    return render_template('service.html', service=service, serviceuser=serviceuser)

@app.route('/servicepageuser', methods=['GET', 'POST'])
@app.route('/servicepageuser/<int:idservice>', methods=['GET', 'POST'])
def servicepageuser(idservice):
    service = Service.query.filter_by(id=idservice).first()
    print service.servicename
    for i in service.users:
        i.username

    return render_template('serviceuser.html', service=service)

@app.route('/addrequest', methods=['GET', 'POST'])
@app.route('/addrequest/<int:idservice>/<int:idservicerequester>', methods=['GET', 'POST'])
def addrequest(idservice, idservicerequester):
    service = Service.query.filter_by(id=idservice).first()
    print service.servicename
    print "The service I juste apply for is", service.servicename
    if service not in current_user.servicerequest:
        current_user.servicerequest.append(service)
        db.session.commit()
        flash('Your request was sent to the user', service.user.username)
        mail = Mail(app)
    else:
        print "ola"
        flash('You already apply')

    return render_template('user_profile.html' )

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/user')
@login_required
def user():
    '''You need to be logged in to access this page'''
    return render_template('user_profile.html')

@app.route('/listservice', methods=['GET', 'POST'])
@login_required
def listservice():
    form = ResearchServiceForm()
    print(form.errors)

    res= Service.query.all()
    notification()
    for r in res:
        print r.servicecity, r.servicetype
        if form.is_submitted():
            print "Ola",form.servicecity.data
        if(form.servicetype.data !='none'):
            print "1"
            if (form.servicename.data != ''):
                print "11"
                if(form.servicecity.data!=""):
                    print "111"
                    if(form.servicedate.data!=None):
                        res = Service.query.filter_by(servicetype=form.servicetype.data, servicename=form.servicename.data, servicecity=form.servicecity.data,servicedate=form.servicedate.data )
                        print "1111"
                    else:
                        print "1112"
                        res = Service.query.filter_by(servicetype=form.servicetype.data, servicename=form.servicename.data, servicecity=form.servicecity.data )
                else:
                    print "112"
                    if (form.servicedate.data != None):
                        print "print 1121"

                        res = Service.query.filter_by(servicetype=form.servicetype.data,  servicename=form.servicename.data, servicedate=form.servicedate.data)
                    else:
                        print "print 1122"
                        res = Service.query.filter_by(servicetype=form.servicetype.data,  servicename=form.servicename.data)
            else:
                print "12"
                if (form.servicecity.data != ""):
                    print "121"
                    if (form.servicedate.data != None):
                        res = Service.query.filter_by(servicetype=form.servicetype.data,
                                                      servicecity=form.servicecity.data,
                                                      servicedate=form.servicedate.data)
                        print "1211"
                    else:
                        print "1212"
                        res = Service.query.filter_by(servicetype=form.servicetype.data,
                                                      servicecity=form.servicecity.data)
                else:
                    print "122"
                    if (form.servicedate.data != None):
                        print "print 1221"

                        res = Service.query.filter_by(servicetype=form.servicetype.data,
                                                      servicedate=form.servicedate.data)
                    else:
                        print "print 1222"
                        res = Service.query.filter_by(servicetype=form.servicetype.data)


        else:
            print "2"
            if (form.servicename.data !=""):
                print "21"
                if (form.servicecity.data != ""):
                    print "211"
                    if (form.servicedate.data != None):
                        print "2111"
                        res = Service.query.filter_by(servicecity=form.servicecity.data, servicename=form.servicename.data, servicedate=form.servicedate.data)
                    else:
                        print "2112"
                        res = Service.query.filter_by(servicecity=form.servicecity.data, servicename=form.servicename.data)
                else:
                    print "212"

                    if (form.servicedate.data != None):
                        print "2121"

                        res = Service.query.filter_by(servicename=form.servicename.data, servicedate=form.servicedate.data)
                        print form.servicedate.data
                    else:
                        print "2122"

                        res = Service.query.filter_by(servicename=form.servicename.data)
            else:
                print "22"
                if (form.servicecity.data != ""):
                    print "221"
                    if (form.servicedate.data != None):
                        print "2211"
                        res = Service.query.filter_by(servicecity=form.servicecity.data,
                                                      servicedate=form.servicedate.data)
                    else:
                        print "2212"
                        res = Service.query.filter_by(servicecity=form.servicecity.data)
                else:
                    print "222"

                    if (form.servicedate.data != None):
                        print "2221"

                        res = Service.query.filter_by(servicedate=form.servicedate.data)
                        print form.servicedate.data
                    else:
                        print "2222"

                        res = Service.query.all()


        for r in res:
            print r.servicecity, r.servicetype


    return render_template('liste_service.html', form=form, res=res)

@app.route('/listserviceuser', methods=['GET', 'POST'])
@login_required
def listserviceuser():
    if current_user.role.name == "User":
        res = Service.query.filter_by(user_id=current_user.id)
    elif current_user.role.name == "Mate":
        res = Service.query.filter_by(mate_id=current_user.id)

    for r in res:
        print r.servicecity, r.servicetype

    return render_template('liste_service_user.html', res=res)

@app.route('/pickmate', methods=['GET', 'POST'])
@app.route('/pickmate/<int:idservice>/<int:idmate>', methods=['GET', 'POST'])
def pickmate(idservice, idmate):
    print idservice
    print idmate
    service = Service.query.filter_by(id=idservice).first()
    print service.servicename
    mate= User.query.filter_by(id=idmate).first()
    print mate.username,  mate.birthdate
    service.mate = mate
    db.session.add(service)
    db.session.commit()
    '''if service.mate is empty:'''


    flash('You have choosen'+mate.username+'for your service'+service.servicename)

    return render_template('user_profile.html' )

@app.route('/test')
def test():
    print "ola"
    return render_template('liste_service.html')

@app.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    form = RegistrationForm()
    roles = {
        'User': (Permission.FOLLOW |
                 Permission.COMMENT |
                 Permission.WRITE_ARTICLES, True),
        'Mate': (Permission.FOLLOW |
                      Permission.COMMENT |
                      Permission.WRITE_ARTICLES |
                      Permission.MODERATE_COMMENTS, False),
        'Administrator': (0xff, False)
    }
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
        role.permissions = roles[r][0]
        role.default = roles[r][1]
        db.session.add(role)
    db.session.commit()

    if form.validate_on_submit():
        if (form.choice.data) == '1':
            role = Role.query.filter_by(name="User").first()

        if (form.choice.data) == '2':
            role = Role.query.filter_by(name="Mate").first()

        print role
        print role.name
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    phone_number=form.phone_number.data,
                    mail=form.mail.data,
                    address=form.address.data,
                    birthdate=form.birthdate.data,
                    roleuser=role
                    )
        user.roleuser.name
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('User succesfully registered', 'success')
        token=user.generate_confirmation_token()
        send_mail('julientriquet69@gmail.com','Confirm your account','confirm',current_user=current_user, token=token)
        flash('A confirmation auth has been sent to you by email')
        return redirect(url_for('loginuser'))

    return render_template('register.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('loginuser'))
    if current_user.confirm(token):
        flash('You have confirm your account. Thanks!')
    else :
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('loginuser'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User logged out!', 'success')
    return render_template('homepage.html')

@app.route('/modifyinformation', methods=['GET', 'POST'])
@login_required
def modifyinformation():
    myForm = ModifyInformationForm()
    if myForm.validate_on_submit():
        current_user.first_name = myForm.first_name.data
        current_user.last_name = myForm.last_name.data
        current_user.phone_number = myForm.phone_number.data
        current_user.mail = myForm.mail.data
        current_user.address = myForm.address.data
        current_user.birthdate = myForm.birthdate.data

        db.session.add(current_user)
        db.session.commit()

        flash('Your profile has been updated.')
        return redirect(url_for('user', username=current_user.username))

    myForm.first_name.data= current_user.first_name
    myForm.last_name.data = current_user.last_name
    myForm.phone_number.data = current_user.phone_number
    myForm.mail.data = current_user.mail
    myForm.address.data = current_user.address
    myForm.birthdate.data = current_user.birthdate


    return render_template('modifyinformation.html', form=myForm)


@app.route('/createservice', methods=['GET', 'POST'])
@login_required
def createservice():
    myForm = CreateServiceForm()
    if myForm.validate_on_submit():
        service = Service(servicetype=myForm.servicetype.data,
                    servicename=myForm.servicename.data,
                    servicedescription=myForm.servicedescription.data,
                    servicedate=myForm.servicedate.data,
                    servicecity=myForm.servicecity.data,

                    user=current_user

                    )
        db.session.add(service)
        print service.user.username
        db.session.commit()
        flash('Profile succesfully updated', 'success')
        return redirect(url_for('user', username=current_user.username))

    return render_template('createservice.html', form=myForm)
