# coding: utf-8
## Created with command: sqlacodegen --flask mysql+pymysql://visualfield:dashgang@146.118.64.10/Dashgang --outfile flaskmodels.py

#from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
# from sqlalchemy.orm import relationship
# from sqlalchemy.schema import FetchedValue
# from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import exists   

from app.extensions import db


class DefectTable(db.Model):
    __tablename__ = 'DefectTable'

    DefectID = db.Column(db.Integer, primary_key=True)
    DefectNumberOf = db.Column(db.Integer, nullable=False)
    DefectCombination = db.Column(db.String(20), nullable=False)


class EyeTable(db.Model):
    __tablename__ = 'EyeTable'

    EyeID = db.Column(db.Integer, primary_key=True)
    EyeSide = db.Column(db.String(10), nullable=False)
    EyeAcuity = db.Column(db.Integer, nullable=False)


class FactTable(db.Model):
    __tablename__ = 'FactTable'

    TestID = db.Column(db.Integer, primary_key=True)
    DefectID = db.Column(db.ForeignKey('DefectTable.DefectID'), nullable=False, index=True)
    HumphreyID = db.Column(db.ForeignKey('HumphreyTable.HumphreyID'), nullable=False, index=True)
    EyeID = db.Column(db.ForeignKey('EyeTable.EyeID'), nullable=False, index=True)
    PatientID = db.Column(db.ForeignKey('PatientTable.PatientID'), nullable=False, index=True)
    ReliabilityID = db.Column(db.ForeignKey('ReliabilityTable.ReliabilityID'), nullable=False, index=True)
    Date = db.Column(db.Date)
    Runtime = db.Column(db.Time)
    Mean_Deviation = db.Column(db.Float)
    Pattern_Deviation = db.Column(db.Float)
    Age = db.Column(db.Integer)

    DefectTable = db.relationship('DefectTable', primaryjoin='FactTable.DefectID == DefectTable.DefectID', backref='fact_tables')
    EyeTable = db.relationship('EyeTable', primaryjoin='FactTable.EyeID == EyeTable.EyeID', backref='fact_tables')
    HumphreyTable = db.relationship('HumphreyTable', primaryjoin='FactTable.HumphreyID == HumphreyTable.HumphreyID', backref='fact_tables')
    PatientTable = db.relationship('PatientTable', primaryjoin='FactTable.PatientID == PatientTable.PatientID', backref='fact_tables')
    ReliabilityTable = db.relationship('ReliabilityTable', primaryjoin='FactTable.ReliabilityID == ReliabilityTable.ReliabilityID', backref='fact_tables')


class HumphreyTable(db.Model):
    __tablename__ = 'HumphreyTable'

    HumphreyID = db.Column(db.Integer, primary_key=True)
    H1 = db.Column(db.String(3))
    H2 = db.Column(db.String(3))
    H3 = db.Column(db.String(3))
    H4 = db.Column(db.String(3))
    H5 = db.Column(db.String(3))
    H6 = db.Column(db.String(3))
    H7 = db.Column(db.String(3))
    H8 = db.Column(db.String(3))
    H9 = db.Column(db.String(3))
    H10 = db.Column(db.String(3))
    H11 = db.Column(db.String(3))
    H12 = db.Column(db.String(3))
    H13 = db.Column(db.String(3))
    H14 = db.Column(db.String(3))
    H15 = db.Column(db.String(3))
    H16 = db.Column(db.String(3))
    H17 = db.Column(db.String(3))
    H18 = db.Column(db.String(3))
    H19 = db.Column(db.String(3))
    H20 = db.Column(db.String(3))
    H21 = db.Column(db.String(3))
    H22 = db.Column(db.String(3))
    H23 = db.Column(db.String(3))
    H24 = db.Column(db.String(3))
    H25 = db.Column(db.String(3))
    H26 = db.Column(db.String(3))
    H27 = db.Column(db.String(3))
    H28 = db.Column(db.String(3))
    H29 = db.Column(db.String(3))
    H30 = db.Column(db.String(3))
    H31 = db.Column(db.String(3))
    H32 = db.Column(db.String(3))
    H33 = db.Column(db.String(3))
    H34 = db.Column(db.String(3))
    H35 = db.Column(db.String(3))
    H36 = db.Column(db.String(3))
    H37 = db.Column(db.String(3))
    H38 = db.Column(db.String(3))
    H39 = db.Column(db.String(3))
    H40 = db.Column(db.String(3))
    H41 = db.Column(db.String(3))
    H42 = db.Column(db.String(3))
    H43 = db.Column(db.String(3))
    H44 = db.Column(db.String(3))
    H45 = db.Column(db.String(3))
    H46 = db.Column(db.String(3))
    H47 = db.Column(db.String(3))
    H48 = db.Column(db.String(3))
    H49 = db.Column(db.String(3))
    H50 = db.Column(db.String(3))
    H51 = db.Column(db.String(3))
    H52 = db.Column(db.String(3))
    H53 = db.Column(db.String(3))
    H54 = db.Column(db.String(3))
    H55 = db.Column(db.String(3))
    H56 = db.Column(db.String(3))
    H57 = db.Column(db.String(3))
    H58 = db.Column(db.String(3))
    H59 = db.Column(db.String(3))
    H60 = db.Column(db.String(3))
    H61 = db.Column(db.String(3))
    H62 = db.Column(db.String(3))
    H63 = db.Column(db.String(3))
    H64 = db.Column(db.String(3))
    H65 = db.Column(db.String(3))
    H66 = db.Column(db.String(3))
    H67 = db.Column(db.String(3))
    H68 = db.Column(db.String(3))
    H69 = db.Column(db.String(3))
    H70 = db.Column(db.String(3))
    H71 = db.Column(db.String(3))
    H72 = db.Column(db.String(3))
    H73 = db.Column(db.String(3))
    H74 = db.Column(db.String(3))
    H75 = db.Column(db.String(3))
    H76 = db.Column(db.String(3))
    H77 = db.Column(db.String(3))


class PatientTable(db.Model):
    __tablename__ = 'PatientTable'

    PatientID = db.Column(db.Integer, primary_key=True)
    PatientCodeName = db.Column(db.String(50))
    PatientCodeDOB = db.Column(db.Float, index=True)


class ReliabilityTable(db.Model):
    __tablename__ = 'ReliabilityTable'

    ReliabilityID = db.Column(db.Integer, primary_key=True)
    ReliabilityExists = db.Column(db.String(3), nullable=False)
    ReliabilityColour = db.Column(db.String(8), nullable=False)
    ReliabilityDesc = db.Column(db.String(50))
    ReliabilityScore = db.Column(db.Integer, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column('ID', db.Integer, primary_key=True, unique=True)
    role = db.Column('Role', db.Enum('doctor', 'researcher', 'admin'))
    username = db.Column('Username', db.String(50))
    password_hash = db.Column('PasswordHash', db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_role(self, role):
        self.role = role

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def has_role(self, role):
        return role in self.role


class InviteKey(db.Model):
    __tablename__ = 'InviteKey'

    id = db.Column('ID', db.Integer, primary_key=True, unique=True)
    invite_key_hash = db.Column('InviteKeyHash', db.String(128))
    role = db.Column('Role', db.Enum('doctor', 'researcher', 'admin'))

    def check_key(key_input):
        # Check if hashed version of key exists in database
        hashed_key_input = generate_password_hash(key_input)
        return db.session.query(db.exists().where(InviteKey.invite_key_hash == hashed_key_input)).scalar()

    def get_key_row(invite_key):
        hashed_invite_key = generate_password_hash(invite_key)
        qry = db.session.query(InviteKey).filter(InviteKey.invite_key_hash == hashed_invite_key)
        return qry.first()

    def set_key(self, key_string):
        self.invite_key_hash = generate_password_hash(key_string)
