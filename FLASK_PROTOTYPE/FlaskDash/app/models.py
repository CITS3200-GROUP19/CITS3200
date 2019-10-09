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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    HashPassword = db.Column(db.String(80))
    role = db.Column(db.Enum('doctor', 'researcher'))

    def set_password(self, password):
        self.HashPassword = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.HashPassword, password)

    def set_role(self, role):
        self.role = role

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Patient(db.Model):
    __tablename__ = 'PatientTable'
    PatientID = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    PatientCodeName = db.Column(db.String(50), index=True, unique=True)
    PatientCodeDOB = db.Column(db.Float, index=True)

