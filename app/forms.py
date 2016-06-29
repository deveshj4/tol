from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField
from wtforms import TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Optional
from app import db, application
from flask import flash, request

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
        confirm_password = self.confirm_password.data
        if password != confirm_password:
            self.confirm_password.errors.append('Passwords do not match')
            return False

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
        return True

class InventoryItemForm(Form):
    name = StringField('Name', validators=[DataRequired()], id='name')
    description = TextAreaField('Description')
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    image = None

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != "" and '.' not in image.filename:
                flash("Invalid image filename")
                return False
            self.image = image

        return True

class SalesItemForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    date = DateField('Date', format="%d/%m/%y", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        return True
