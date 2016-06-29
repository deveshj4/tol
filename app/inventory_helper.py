from flask import jsonify
from models import Item, Sale
from app import db, cloudinaryDB

def add_inventory_item_html(form):
    name = form.name.data.strip()
    description = form.description.data.strip()
    quantity = form.quantity.data
    price = form.price.data

    item = Item.query.filter_by(name=name).first()
    if item is None:
        item = Item(name=name, description=description, quantity=quantity,
                    price=price)
        db.session.add(item)
    else:
        item.name = name
        item.quantity = quantity
        item.price = price
        if description != "":
            item.description = description
    if form.image is not None:
        item.image_name = item.name
        cloudinaryDB.upload_image(form.image, item.image_name)
    db.session.commit()
    return True

def add_sales_item_html(form):
    name = form.name.data.strip()
    quantity = form.quantity.data
    price = form.price.data
    date = form.date.data

    item = Item.query.filter_by(name=name).first()
    sale = Sale(item_id=item.get_id(), quantity=quantity, price=price,
                date=date)
    item.quantity -= quantity
    db.session.add(sale)
    db.session.commit()
    return True

def add_inventory_item_json(data):
    name = data['name']
    description = data['description']
    quantity = int(data['quantity'])
    price = int(data['price'])

    item = Item.query.filter_by(name=name).first()
    if item is None:
        item = Item(name=name, description=description, quantity=quantity,
                    price=price)
        db.session.add(item)
    else:
        item.name = name
        item.quantity = quantity
        item.price = price
        if description != "":
            item.description = description
    db.session.commit()
    return jsonify(status="success")

def add_sales_item_json(data):
    name = data['name']
    quantity = int(data['quantity'])
    price = int(data['price'])
    date = data['date']

    item = Item.query.filter_by(name=name).first()
    sale = Sale(item_id=item.get_id(), quantity=quantity, price=price,
                date=date)
    item.quantity -= quantity
    db.session.add(sale)
    db.session.commit()
    return jsonify(status="success")
