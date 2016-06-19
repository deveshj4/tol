from models import User
from flask import jsonify, make_response
from app import db, application
from werkzeug.security import generate_password_hash, check_password_hash

def validate_html_register(form):
    password = form.password.data
    email = form.email.data.strip()
    firstname = form.firstname.data.strip()
    lastname = form.lastname.data.strip()
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, firstname=firstname,
                    lastname=lastname,
                    password=generate_password_hash(password))
        if application.config['ADMIN_PASSWORD'] == password:
            user.is_admin = True
        db.session.add(user)
        db.session.commit()
    else:
        form.email.errors.append('Email already exists. If you are an \
                                 existing user, please sign in.')
        return False

    form.user = user
    return True

def validate_html_login(form):
    password = form.password.data
    email = form.email.data.strip()
    user = User.query.filter_by(email=email).first()
    if user is None:
        form.email.errors.append('Email not found. If you are a new \
                                 user, please register.')
        return False
    elif not check_password_hash(user.password, password):
        form.password.errors.append('Incorrect Password Entered.')
        return False

    form.user = user
    return True

def validate_json_register(data):
    user = User.query.filter_by(email=data['email']).first()
    if user is not None:
        return None, jsonify(status='failed', error="user already registered",
                             error_field="email")
    user = User(email=data['email'], firstname=data['firstname'],
                lastname=data['lastname'],
                password=generate_password_hash(data['password']))
    if application.config['ADMIN_PASSWORD'] == data['password']:
        user.is_admin = True
    db.session.add(user)
    db.session.commit()
    return user, jsonify(status='success', user=repr(user))

def validate_json_login(data):
    user = User.query.filter_by(email=data['email']).first()
    if user is not None:
        if check_password_hash(user.password, data['password']):
            return user, jsonify(status='success', user=repr(user))
        else:
            return None, jsonify(status='failed', error="Invalid email and \
                           password combination", error_field="password")
    return None, jsonify(status='failed', error="user not found",
                         error_field="email")
