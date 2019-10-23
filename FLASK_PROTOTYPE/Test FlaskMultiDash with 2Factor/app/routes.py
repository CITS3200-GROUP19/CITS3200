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
from werkzeug.security import check_password_hash

import string
import random

from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView

from app.forms import LoginForm, RegistrationForm
from app.models import User, InviteKey
from app.extensions import db
from app.extensions import limiter

server_mod = Blueprint("main", __name__)


# Helper method for admin keygen buttons that returns randomised 10 character alphanumerical string
# Stores hash of this string in db
def key_generator(selected_role):
    lettersAndDigits = string.ascii_letters + string.digits
    generated_key = "".join(random.choice(lettersAndDigits) for i in range(10))
    # Check generated key not in db already
    while InviteKey.get_key_row(generated_key):
        generated_key = "".join(random.choice(lettersAndDigits) for i in range(10))

    invite_key = InviteKey(role=selected_role)
    invite_key.set_key(generated_key)
    db.session.add(invite_key)
    db.session.commit()
    return generated_key


@server_mod.route("/")
@limiter.exempt
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    else:
        return redirect(url_for("main.login"))


@server_mod.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(
            user.password_hash, form.password.data
        ):
            error = "Invalid username or password"
            return render_template("login.html", form=form, error=error)

        login_user(user, remember=form.remember.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@server_mod.route("/logout")
@login_required
@limiter.exempt
def logout():
    logout_user()

    return redirect(url_for("main.index"))


@server_mod.route("/user_profile")
@login_required
@limiter.exempt
def user_profile():
    return render_template(
        "user_profile.html", name=current_user.username, role=current_user.role
    )


@server_mod.route("/home")
@login_required
@limiter.exempt
def home():
    return render_template("home.html")  # , name=current_user.username)


@server_mod.route("/about")
@login_required
@limiter.exempt
def about():
    return render_template("about.html")  # , name=current_user.username)


@server_mod.route("/admin", methods=["GET", "POST"])
@login_required
@limiter.exempt
def admin():
    # if (current_user.is_authenticated and current_user.role == 'admin'):
    if current_user.is_authenticated:
        return "admin"
    else:
        form = LoginForm()
        error = "Please log in"
        return render_template("login.html", form=form, error=error)


class MyAdminIndexView(AdminIndexView):
    decorators = [limiter.exempt]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("main.login", next=request.url))


class MyModelView(ModelView):
    decorators = [limiter.exempt]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.admin"))


class NewView(BaseView):
    decorators = [limiter.exempt]

    @expose("/")
    def index(self):
        return redirect(url_for("main.index"))


class DoctorKeyGen(BaseView):
    decorators = [limiter.exempt]

    @expose("/")
    def index(self):
        generated_key = key_generator("doctor")
        flash(
            "Your generated {role} invite key is {key}".format(
                key=generated_key, role="doctor"
            )
        )
        return redirect(url_for("main.admin"))


class ResearcherKeyGen(BaseView):
    decorators = [limiter.exempt]

    @expose("/")
    def index(self):
        generated_key = key_generator("researcher")
        flash(
            "Your generated {role} invite key is {key}".format(
                key=generated_key, role="researcher"
            )
        )
        return redirect(url_for("main.admin"))


@server_mod.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check invite key
        invite_key = InviteKey.get_key_row(form.invite_key.data)
        if invite_key is None:
            error = "Invalid invite key"
            return render_template("register.html", form=form, error=error)
        if invite_key.role != form.role.data:
            error = "This invite key cannot be used for the selected role"
            return render_template("register.html", form=form, error=error)

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.set_role(form.role.data)
        db.session.add(user)

        # Delete invite key in database onced used for registration
        if invite_key:
            db.session.delete(invite_key)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html", title="Register", form=form)
