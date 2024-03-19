from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from flask import jsonify
import requests


def get_user_id(username):
    user = User.query.filter(User.username == username).first()
    return user.id


def add_reminder(username, product_id, quantity):
    user_id = get_user_id(username)
    new_quantity = quantity if quantity != '' else 1
    new_reminder = Reminder(
        user_id=user_id, product_id=product_id, quantity=new_quantity)
    db.session.add(new_reminder)
    db.session.commit()
    return jsonify(reminder=new_reminder.serialize())


def get_reminders(username):
    user_id = get_user_id(username)
    all_reminders = db.session.query(Product.id, Product.product_name, ProductCategory.category_name, Reminder.id, Reminder.user_id,
                                     Reminder.product_id, Reminder.quantity).join(Reminder).join(ProductCategory).filter(Reminder.user_id == user_id).all()
    return [reminder._asdict() for reminder in all_reminders]


def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()


def update_reminder(id, quantity):
    reminder = Reminder.query.get_or_404(id)
    reminder.quantity = quantity
    db.session.commit()
    return jsonify(reminder=reminder.serialize())
