from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from flask import jsonify
import requests

def get_product_categories():
    return [category.serialize() for category in ProductCategory.query.all()]

def find_product(product_name, category_id):
    find_product =  Product.query.filter(Product.product_name == product_name, Product.category_id==category_id).all()
    return find_product

def add_product(product_name, category_id):
    new_product = Product(product_name=product_name, category_id=category_id)
    db.session.add(new_product)
    db.session.commit()
    return jsonify(product=new_product.serialize())
