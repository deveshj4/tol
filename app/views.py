from app import application, db, lm, cloudinaryDB
from flask import render_template, redirect, flash, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm
from models import User, Item, Sale

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
    user = g.user
    return render_template("index.html",
                            title='Home',
                            user=user)

@application.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('register.html',
                            title='Register',
                            form=form)

@application.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html',
                            title='Sign In',
                            form=form)

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/inventory', methods = ['GET', 'POST'])
def inventory():
    items = Item.query.all()
    if request.method == 'POST':
        item = Item()
        db.session.add(item)
        db.session.commit()
    return render_template("inventory.html",
                           title='Inventory',
                           items=items)

@application.route('/sales', methods = ['GET', 'POST'])
def sales():
    sales = Sale.query.all()
    if request.method == 'POST':
        sale = Sale()
        db.session.add(sale)
        db.session.commit()
    return render_template("sales.html",
                           title='Sales',
                           sales=sales)
