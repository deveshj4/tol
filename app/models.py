from app import db, cloudinaryDB
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password = db.Column(db.String(120), index=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
            return str(self.id) # python 3

    def __repr__(self):
        return '<User %r>' % (self.first_name)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False, unique=True)
    description = db.Column(db.String(250))
    image_url = db.Column(db.String(120))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    sales = db.relationship('Sale', backref='item', lazy='dynamic')

    def get_id(self):
            return str(self.id) # python 3

    def image(self, size):
        return cloudinaryDB.compose_url(self.image_url, size)

    def __repr__(self):
        return '<Item %r, Price %d>' % (self.name, self.price)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, index=True, nullable=False)
