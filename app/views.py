from app import application, db, lm, cloudinaryDB
from flask import render_template, redirect, flash, session, url_for, request
from flask import g, abort, make_response, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm, InventoryItemForm, SalesItemForm
from models import User, Item, Sale
from functools import wraps
from login_helper import *
from inventory_helper import *

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not g.user.is_admin:
                abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def is_json_request():
    if 'json' in request.headers.get('Accept'):
        return True
    return False

@application.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@application.route('/')
@application.route('/index')
@login_required
def index():
    if is_json_request():
        return jsonify(user=repr(g.user))
    else:
        return render_template("index.html",
                                title='Home',
                                user=g.user)

@application.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        if is_json_request():
            return jsonify(status='failed', error='user already logged in',
                           user=repr(g.user))
        else:
            return redirect(url_for('index'))
    if is_json_request():
        user, response = validate_json_register(request.get_json())
        if user is not None:
            login_user(user)
        return response
    form = RegisterForm()
    if form.validate_on_submit() and validate_html_register(form):
        login_user(form.user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('register.html',
                            title='Register',
                            form=form)

@application.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        if is_json_request():
            return jsonify(status='failed', error='user already logged in',
                            user=repr(user))
        else:
            return redirect(url_for('index'))
    if is_json_request():
        user, response = validate_json_login(request.get_json())
        if user is not None:
            login_user(user)
        return response
    form = LoginForm()
    if form.validate_on_submit() and validate_html_login(form):
        login_user(form.user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html',
                            title='Sign In',
                            form=form)

@application.route('/logout')
def logout():
    logout_user()
    if is_json_request():
        return jsonify(status='success')
    return redirect(url_for('index'))

@application.route('/inventory')
@login_required
@roles_required('admin')
def inventory():
    items = Item.query.all()
    if is_json_request():
        items = "[" + ','.join([repr(item) for item in items]) + "]"
        return jsonify(status='success', items=items)
    return render_template('inventory.html',
                            title='Inventory',
                            items=items)

@application.route('/inventory/update', methods = ['GET', 'POST'])
@login_required
@roles_required('admin')
def inventory_update():
    if is_json_request():
        if request.method == 'GET':
            abort(400)
        else:
            return add_inventory_item_json(request.get_json())
    form = InventoryItemForm()
    if form.validate_on_submit() and add_inventory_item_html(form):
        return redirect(request.args.get('next') or url_for('inventory'))
    return render_template('inventory_update.html',
                            title='Inventory',
                            form=form)

@application.route('/sales')
@login_required
@roles_required('admin')
def sales():
    sales = Sale.query.all()
    if is_json_request():
        sales = "[" + ','.join([repr(sale) for sale in sales]) + "]"
        return jsonify(status='success', sales=sales)
    return render_template('sales.html',
                            title='Sales',
                            sales=sales)

@application.route('/sales/update', methods = ['GET', 'POST'])
@login_required
@roles_required('admin')
def sales_update():
    if is_json_request():
        if request.method == 'GET':
            abort(400)
        else:
            return add_sales_item_json(request.get_json())
    form = SalesItemForm()
    if form.validate_on_submit() and add_sales_item_html(form):
        return redirect(request.args.get('next') or url_for('sales'))
    return render_template('sales_update.html',
                            title='Sales',
                            form=form)

def handle_error(errnum, errmsg):
    if is_json_request():
        return make_response(jsonify(error=errmsg), errnum)
    else:
        return make_response(render_template('error.html', error=errmsg),
                             errnum)

@application.errorhandler(404)
def not_found(error):
    handle_error(404, "File Not Found")

@application.errorhandler(401)
def not_found(error):
    handle_error(401, "Access Denied")

@application.errorhandler(400)
def not_found(error):
    handle_error(400, "Bad Request")
