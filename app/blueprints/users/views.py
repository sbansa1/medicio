from flask import render_template, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app.blueprints.users import auth
from app.blueprints.users.forms import LoginForm, RegistrationFormUser, ResetPasswordRequestForm, ResetPasswordForm
from app.blueprints.users.model import UserResource
from flask_login import current_user, login_user, logout_user, login_required
from app.extensions import db

@auth.route("/")
def index():
    return render_template('index/index.html')

@auth.route("/login", methods=['GET','POST'])
def login():
    """End point for Login"""

    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserResource.check_user_identity(identity=form.email.data)
        if user is None or not user.decrypt_password(password=form.password.data):
            flash( 'Invalid email or password' )
            return redirect(url_for('user.login'))
        login_user(user)
        next_page = request.args.get('next_page')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user.index')
        return redirect(next_page)
        return redirect(url_for('user.index'))
    return render_template('user/login.html', title='Sign In', form=form)



@auth.route("/register", methods=['GET','POST'])
def registration():
    """End point for Registration"""

    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = RegistrationFormUser()

    if form.validate_on_submit():
        data = {"name":form.name.data,"email":form.email.data,"password":form.password.data,
                "address_1":form.address_1.data,"address_2":form.address_2.data,
                "city":form.city.data,"postal_code":form.postal_code.data,"mob_phone":form.mobile_phone.data,
                "role":form.roles.data}

        user = UserResource(**data)
        user.save()
        flash("Congratulations you have have successfully registered")
        return redirect(url_for('user.login'))
    return render_template('user/registration.html', title='Sign Up', form=form)


@auth.route("/logout", methods=['GET','POST'])
def logout():
    """Logs the user out"""

    logout_user()
    return redirect(url_for('user.index'))



@user.route("/reset_password", methods=['GET','POST'])
def reset_password_request():
    """Reset Password Request"""

    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = UserResource.check_user_identity(identity=form.email.data)
        print(form.email.data)
        if user:
            UserResource.send_reset_password_mail(identity=user)
        flash( 'Check your email for the instructions to reset your password' )
        return redirect(url_for('user.login'))

    return render_template(template_name_or_list='user/reset_password_request.html',
                           title="Reset Password", form=form)



@auth.route("/reset_password/<token>", methods=['GET','POST'])
def verify_password_reset_token(token):
    """This end points verifies the password reset token"""
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    user = UserResource.decode_token(token=token)
    if not user:
        return redirect(url_for('user.index'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        """Resets the user password"""
        UserResource.set_password(password=form.password.data)
        db.session.commit()
        flash('The password has been successfuly reset')
        return redirect(url_for('user.login'))
    return render_template(template_name_or_list='user/reset_password.html', form=form)




@auth.route("/profile/<username>",methods=['GET','POST'])
@login_required
def profile_page(username):
    """The profile page"""

    user = UserResource.check_user_identity(identity=username)

    return render_template('user/user_profile.html', user=user, title="Profile Page")




