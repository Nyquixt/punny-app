from flask import Blueprint, render_template, url_for, redirect, \
    session, request, send_from_directory, abort, flash

from user.forms import LoginForm, RegisterForm
from user.models import User
from utility.decorators import login_required
# outside import
import bcrypt

user_app = Blueprint('user_app', __name__)

@user_app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            salt = bcrypt.gensalt()
            user = User(
                username = form.username.data,
                password = bcrypt.hashpw(form.password.data, salt)
            ).save()

            return redirect(url_for('user_app.login'))
    
    return render_template('user/register.html', form=form)


@user_app.route('/login', methods=['GET', 'POST'])
def login():

    # login form class from forms.py
    form = LoginForm()

    # if no validation errors search for user
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects.filter(
                username=form.username.data.lower().strip()
            ).first()
            # if user exist check password
            if user:
                if bcrypt.hashpw(form.password.data, user.password) == user.password:
                    session['username'] = form.username.data  # set the session variables
                    return redirect(url_for('general_app.index'))
                else:
                    return render_template('user/login.html', error='Incorrect username or password')
            # user does not exist
            else:
                return render_template('user/login.html', error='Not a valid username. Register?')

    return render_template('user/login.html', form=form)

@login_required
@user_app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('general_app.index'))