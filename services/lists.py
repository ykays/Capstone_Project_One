from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from flask import jsonify
import requests


def get_user_id(username):
    user = User.query.filter(User.username == username).first()
    return user.id


def get_user_template_id(username):
    user = User.query.filter(User.username == username).first()
    template = ListTemplate.query.filter(
        ListTemplate.user_id == user.id).first()
    if template is None:
        return False
    return template.id


def get_user_grocery_list_id(username, date):
    user_id = get_user_id(username)
    list = GroceryList.query.filter(
        GroceryList.user_id == user_id, GroceryList.date == date).first()
    return list.id


def check_grocery_list_exist(username, date):
    user_id = get_user_id(username)
    list = GroceryList.query.filter(
        GroceryList.user_id == user_id, GroceryList.date == date).all()
    return len(list) != 0


def change_format(obj):
    return [item._asdict() for item in obj]


def add_new_grocery_list(username, date):
    user_id = get_user_id(username)
    template_id = get_user_template_id(username)
    list_id = insert_new_grocery_list(user_id, date, template_id)
    template_products = get_all_template_products(template_id, date)
    update_glp = insert_grocery_list_products(template_products)
    grocery_list_products = get_all_products_list(list_id, date)
    return grocery_list_products

# date (GL), product name, quantity, category


def insert_new_grocery_list(user_id, date, template_id):
    new_list = GroceryList(user_id=user_id, date=date, template_id=template_id)
    db.session.add(new_list)
    db.session.commit()
    return new_list.id


def get_all_template_products(template_id, date):
    new_list_products = db.session.query(ListTemplate.id, GroceryList.id, GroceryList.template_id, TemplateProduct.product_id).join(
        GroceryList).join(TemplateProduct).filter(ListTemplate.id == template_id, GroceryList.date == date).all()
    return [product._asdict() for product in new_list_products]


def insert_grocery_list_products(products):
    all_glp = []
    for product in products:
        new_glp = GroceryListProducts(
            grocery_list_id=product['id'], product_id=product['product_id'])
        all_glp.append(new_glp)

    db.session.bulk_save_objects(all_glp)
    db.session.commit()
    return all_glp


def get_all_products_list(list_id, date):
    grocery_list_products_db = db.session.query(GroceryListProducts.id, GroceryListProducts.product_id, GroceryListProducts.grocery_list_id, GroceryListProducts.quantity, GroceryListProducts.bought, GroceryList.date, GroceryList.total_price, Product.product_name,
                                                Product.category_id, ProductCategory.category_name).join(GroceryList).join(Product).join(ProductCategory).filter(GroceryListProducts.grocery_list_id == list_id, GroceryList.date == date).order_by(Product.category_id, Product.product_name).all()
    return change_format(grocery_list_products_db)


def get_all_reminders(username):
    user_id = get_user_id(username)
    user_reminders = Reminder.query.filter(Reminder.user_id == user_id).all()
    reminders = []
    if len(user_reminders) == 0:
        return []
    for reminder in user_reminders:
        reminders.append({
            "id": reminder.id,
            "product_id": reminder.product_id,
            "quantity": reminder.quantity
        })
    return reminders


def compare_reminders_with_current_list(username, date):
    list_id = get_user_grocery_list_id(username, date)
    list_products = get_all_products_list(list_id, date)
    list_reminders = get_all_reminders(username)
    if len(list_reminders) == 0:
        return False
    list_products_ids = [product['product_id'] for product in list_products]

    for reminder in list_reminders:
        if reminder["product_id"] in list_products_ids:
            glp = GroceryListProducts.query.filter(
                GroceryListProducts.product_id == reminder["product_id"], GroceryListProducts.grocery_list_id == list_id).first()
            glp.quantity = reminder['quantity']
        else:
            glp = GroceryListProducts(
                grocery_list_id=list_id, product_id=reminder["product_id"], quantity=reminder['quantity'])
            db.session.add(glp)
        db.session.commit()

    delete_user_reminders = delete_reminders(list_reminders)
    return True


def delete_reminders(list_reminders):
    for reminder in list_reminders:
        reminder = Reminder.query.get_or_404(reminder['id'])
        db.session.delete(reminder)
    db.session.commit()
    return True


def get_user_list_products(username, date):
    check_list_exists = check_grocery_list_exist(username, date)
    if check_list_exists:
        list_id = get_user_grocery_list_id(username, date)
        list_products = get_all_products_list(list_id, date)
        return jsonify(list=list_products)

    check_template_exists = get_user_template_id(username)
    if not check_template_exists:
        return jsonify(message='Template needed')

    new_list = add_new_grocery_list(username, date)
    return (jsonify(list=new_list), 201)


def add_new_product(username, date, product_id, quantity):
    list_id = get_user_grocery_list_id(username, date)
    new_quantity = quantity if quantity != '' else 1
    new_glp = GroceryListProducts(
        grocery_list_id=list_id, product_id=product_id, quantity=new_quantity)
    db.session.add(new_glp)
    db.session.commit()
    return jsonify(product=new_glp.serialize())


def delete_list_product(id):
    list_product = GroceryListProducts.query.get_or_404(id)
    db.session.delete(list_product)
    db.session.commit()


def update_product_quantity(id, quantity, bought):
    list_product = GroceryListProducts.query.get_or_404(id)
    list_product.quantity = quantity if quantity != None else list_product.quantity
    list_product.bought = bought if bought != None else list_product.bought
    db.session.commit()
    return jsonify(list_product=list_product.serialize())


def update_price_grocery_list(username, date, price):
    user_id = get_user_id(username)
    grocery_list = GroceryList.query.filter(
        GroceryList.user_id == user_id, GroceryList.date == date).first()
    grocery_list.total_price = 0 if price == '' else price

    db.session.commit()
    return jsonify(message="The price has been updated")
