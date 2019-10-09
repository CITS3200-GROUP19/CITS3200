from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import db
# from app.extensions import login_manager


# @login.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(80))
    role = db.Column(db.Enum('doctor', 'researcher'))

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
    PatientID = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    PatientCodeName = db.Column(db.String(50), index=True, unique=True)
    PatientCodeDOB = db.Column(db.Float, index=True)

##for rest of the data @@@@@@@@@----------------@@@@@@@@

class FactTable(db.Model):
    TestID = db.Column(db.Integer, primary_key=True)
    HumphreyID = db.Column(db.Integer, db.ForeignKey('HumphreyTable.HumphreyID')) ##why not make this testID?
    EyeID = db.Column(db.Integer, db.ForeignKey('EyeTable.EyeID'))
    DefectID = db.Column(db.Integer, db.ForeignKey('DefectsTable.DefectID'))
    ReliabilityID = db.Column(db.Integer, db.ForeignKey('ReliabilityTable.ReliabilityID'))
    ##PatientID = db.Column(db.Integer, db.ForeignKey('PatientTable.PatientID'))
    ##Data/Facts
    Runtime = db.Column(db.Integer) ##not sure
    Mean_Deviation = db.Column(db.Float)
    Pattern_Deviation = db.Column(db.Float)
    Age = db.Column(db.Integer)

    def __init__(self, Runtime, Mean_Deviation, Pattern_Deviation, Age):
        self.Runtime = Runtime
        self.Mean_Deviation = Mean_Deviation
        self.Pattern_Deviation = Pattern_Deviation
        self.Age = Age

class EyeTable(db.Model):
    EyeID = db.Column(db.Integer, primary_key = True) ## o is left eye, 1 is right eye
    EyeSide = db.Column(db.String(20))
    EyeAcuity = db.Column(db.Integer)

class DefectTable(db.Model):
    DefectID = db.Column(db.Integer, primary_key = True)
    DefectNumberOf = db.Column(db.Integer)
    DefectCombination = db.Column(db.String(100))


class ReliabilityTable(db.Model):
    ReliabilityID = db.Column(db.Integer, primary_key = True)
    ReliabilityGiven = db.Column(db.Integer)
    ReliabilityColour = db.Column(db.String(20))
    ReliabilityDesc = db.Column(db.String(200))
    ReliabilityScore = db.Column(db.Integer)

    #in unbuntu:
    ##from Main import db
    ##db.create_all

class HumphreyTable(db.Model):
    HumpreyID = db.Column(db.Integer, primary_key = True)
    H1 = db.Column(db.Integer)
    H2 = db.Column(db.Integer)
    H3 = db.Column(db.Integer)
    H4 = db.Column(db.Integer)
    H5 = db.Column(db.Integer)
    H6 = db.Column(db.Integer)
    H6 = db.Column(db.Integer)
    H7 = db.Column(db.Integer)
    H8 = db.Column(db.Integer)
    H9 = db.Column(db.Integer)
    H10 = db.Column(db.Integer)
    H11 = db.Column(db.Integer)
    H12 = db.Column(db.Integer)
    H13 = db.Column(db.Integer)
    H14 = db.Column(db.Integer)
    H15 = db.Column(db.Integer)
    H16 = db.Column(db.Integer)
    H17 = db.Column(db.Integer)
    H18 = db.Column(db.Integer)
    H19 = db.Column(db.Integer)
    H20 = db.Column(db.Integer)
    H21 = db.Column(db.Integer)
    H22 = db.Column(db.Integer)
    H23 = db.Column(db.Integer)
    H24 = db.Column(db.Integer)
    H25 = db.Column(db.Integer)
    H26 = db.Column(db.Integer)
    H27 = db.Column(db.Integer)
    H28 = db.Column(db.Integer)
    H29 = db.Column(db.Integer)
    H30 = db.Column(db.Integer)
    H31 = db.Column(db.Integer)
    H32 = db.Column(db.Integer)
    H33 = db.Column(db.Integer)
    H34 = db.Column(db.Integer)
    H35 = db.Column(db.Integer)
    H36 = db.Column(db.Integer)
    H37 = db.Column(db.Integer)
    H38 = db.Column(db.Integer)
    H39 = db.Column(db.Integer)
    H40 = db.Column(db.Integer)
    H41 = db.Column(db.Integer)
    H42 = db.Column(db.Integer)
    H43 = db.Column(db.Integer)
    H44 = db.Column(db.Integer)
    H45 = db.Column(db.Integer)
    H46 = db.Column(db.Integer)
    H47 = db.Column(db.Integer)
    H48 = db.Column(db.Integer)
    H50 = db.Column(db.Integer)
    H51 = db.Column(db.Integer)
    H52 = db.Column(db.Integer)
    H53 = db.Column(db.Integer)
    H54 = db.Column(db.Integer)
    H55 = db.Column(db.Integer)
    H56 = db.Column(db.Integer)
    H57 = db.Column(db.Integer)
    H58 = db.Column(db.Integer)
    H59 = db.Column(db.Integer)
    H60 = db.Column(db.Integer)
    H61 = db.Column(db.Integer)
    H62 = db.Column(db.Integer)
    H63 = db.Column(db.Integer)
    H64 = db.Column(db.Integer)
    H65 = db.Column(db.Integer)
    H66 = db.Column(db.Integer)
    H67 = db.Column(db.Integer)
    H68 = db.Column(db.Integer)
    H69 = db.Column(db.Integer)
    H70 = db.Column(db.Integer)
    H71 = db.Column(db.Integer)
    H72 = db.Column(db.Integer)
    H73 = db.Column(db.Integer)
    H74 = db.Column(db.Integer)
    H75 = db.Column(db.Integer)
    H76 = db.Column(db.Integer)
