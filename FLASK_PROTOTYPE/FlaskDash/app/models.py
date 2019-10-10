from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import db
# from app.extensions import login_manager


# @login.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column('ID', db.Integer, primary_key=True, unique=True)
    username = db.Column('Username', db.String(64), index=True, unique=True)
    password_hash = db.Column('HashPassword', db.String(80))
    role = db.Column('Role', db.Enum('doctor', 'researcher'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_role(self, role):
        self.role = role

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Patient(db.Model):
    __tablename__ = 'PatientTable'
    id = db.Column('PatientID', db.Integer, primary_key=True, index=True, unique=True)
    code_name = db.Column('PatientCodeName', db.String(50), index=True, unique=True)
    code_dob = db.Column('PatientCodeDOB', db.Float, index=True)
