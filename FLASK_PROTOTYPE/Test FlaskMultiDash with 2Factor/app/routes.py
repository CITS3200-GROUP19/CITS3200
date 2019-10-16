from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash

import string
import random

from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView

from app.forms import LoginForm, RegistrationForm, KeyGenForm
from app.models import User, InviteKey
from app.extensions import db

server_mod = Blueprint('main', __name__)


@server_mod.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.login'))


@server_mod.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@server_mod.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))


@server_mod.route('/user_profile')
@login_required
def user_profile():
    return render_template('user_profile.html', name=current_user.username, role=current_user.role)

@server_mod.route('/home')
@login_required
def home():
    return render_template('home.html')#, name=current_user.username)

@server_mod.route('/about')
@login_required
def about():
    return render_template('about.html')#, name=current_user.username)


@server_mod.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
#    if (current_user.is_authenticated and current_user.role == 'doctor'):
   if (current_user.is_authenticated):
       return 'admin'
   else:
       form = LoginForm()
       error = 'Please log in'
       return render_template('login.html', form=form, error=error)


class MyModelView(ModelView):
    def is_accessible(self):
        # if (current_user.is_authenticated and current_user.role == 'doctor'):
        if (current_user.is_authenticated):
            return True
        # elif (current_user.is_authenticated and current_user.role == 'researcher'):
            # return False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.admin'))


class NewView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('main.index'))

class KeyGenView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('main.keygen'))
        # form = KeyGenForm()
        # if form.validate_on_submit():
        #     # return self.render('admin/keygen.html')

        #     #Generate a random string of letters and digits
        #     lettersAndDigits = string.ascii_letters + string.digits
        #     generated_key = ''.join(random.choice(lettersAndDigits) for i in range(10))
        #     while (InviteKey.check_key(generated_key)):
        #         generated_key = ''.join(random.choice(lettersAndDigits) for i in range(10))
        #     flash("Your generated invite key is {key}".format(key=generated_key))

        #     # Check generated key not in db already
        #     invite_key = InviteKey(role=form.role.data)
        #     invite_key.set_key(generated_key)
        #     db.session.add(invite_key)
        #     db.session.commit()

        #     return render_template('admin/keygen.html', form=form)

        # return redirect(url_for('main.admin'))

# Currently role is not added to generated key due to form.validate_on_submit(): not working
@server_mod.route('/keygen', methods=['GET', 'POST'])
@login_required
def keygen():
    if (current_user.is_authenticated):
        form = KeyGenForm()
        # if form.validate_on_submit():

            # Generate a random string of letters and digits
        lettersAndDigits = string.ascii_letters + string.digits
        generated_key = ''.join(random.choice(lettersAndDigits) for i in range(10))
        while (InviteKey.check_key(generated_key)):
            generated_key = ''.join(random.choice(lettersAndDigits) for i in range(10))
        flash("Your generated invite key is {key} with role {role}".format(key=generated_key, role=form.role.data))

        # Check generated key not in db already
        invite_key = InviteKey(role=form.role.data)
        invite_key.set_key(generated_key)
        db.session.add(invite_key)
        db.session.commit()
        return redirect(url_for('main.admin'))
    else:
        form = LoginForm()
        error = 'Please log in'
        return render_template('login.html', form=form, error=error)


@server_mod.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check invite key
        if not InviteKey.check_key(form.invite_key.data):
            error = 'Invalid invite key'
            return render_template('register.html', form=form, error=error)

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.set_role(form.role.data)
        db.session.add(user)

        # Delete invite key in database onced used for registration
        invite_key = InviteKey.get_key_row(form.invite_key.data)
        if invite_key:
            db.session.delete(invite_key)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)


## Don't need? ##

# @server_mod.route('/admin_login', methods=['GET', 'POST'])
# def admin_login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password, form.password.data):
#                 login_user(user, remember=form.remember.data)
#                 return redirect(url_for('/admin'))

#         return '<h1>Invalid username or password</h1>'

#     return render_template('admin_login.html', form=form)
