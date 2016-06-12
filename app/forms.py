from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email
from app import db, application
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request

class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired()])
    firstname = StringField('FirstName', validators=[DataRequired()])
    lastname = StringField('LastName', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        password = self.password.data
        confirm_password = self.password.data
        email = self.email.data.strip()
        firstname = self.firstname.data.strip()
        lastname = self.lastname.data.strip()
        user = User.query.filter_by(email=email).first()
        if user is None:
            if password != confirm_password:
                self.confirm_password.errors.append('Passwords do not match')
                return False
            user = User(email=email, firstname=firstname,
                        lastname=lastname,
                        password=generate_password_hash(password))
            if application.config['ADMIN_PASSWORD'] == password:
                user.is_admin = True
            db.session.add(user)
            db.session.commit()
        else:
            self.email.errors.append('Email already exists. If you are an \
                                     existing user, please sign in.')
            return False

        self.user = user
        return True

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        password = self.password.data
        email = self.email.data.strip()
        user = User.query.filter_by(email=email).first()
        if user is None:
            self.email.errors.append('Email not found. If you are a new \
                                     user, please register.')
            return False
        elif not check_password_hash(user.password, password):
            self.password.errors.append('Incorrect Password Entered.')
            return False

        self.user = user
        return True
