from flask import render_template, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app.blueprints.users import user
from app.blueprints.users.forms import LoginForm, RegistrationFormUser
from app.blueprints.users.model import User
from flask_login import current_user,login_user,logout_user
from app.extensions import db

@user.route("/")
def index():
    return render_template('index/index.html')

@user.route("/login", methods=['GET','POST'])
def login():
    """End point for Login"""

    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.check_user_identity(identity=form.email.data)
        if user is None or not user.decrypt_password(password=form.password.data):
            flash( 'Invalid email or password' )
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next_page')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        return redirect(url_for('user.index'))
    return render_template('user/login.html', title='Sign In', form=form)



@user.route("/register", methods=['GET','POST'])
def registration():
    """End point for Registration"""

    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = RegistrationFormUser()

    if form.validate_on_submit():
        data = {"name":form.name.data,"email":form.email.data,"password":form.password.data,
                "address_1":form.address_1.data,"address_2":form.address_2.data,
                "city":form.city.data,"postal_code":form.postal_code.data,"mob_phone":form.mobile_phone.data}
        user = User(**data)
        user.save()
        flash("Congratulations you have have successfully registered")
        return redirect(url_for('user.login'))
    return render_template('user/registration.html', title='Sign Up', form=form)


@user.route("/logout", methods=['GET','POST'])
def logout():
    """Logs the user out"""

    logout_user()
    return redirect(url_for('user.index'))











