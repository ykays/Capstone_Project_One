from flask import Blueprint, Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
import requests
import dotenv
import os
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from functools import wraps
import services
from app_util.logged import logged_in


external_search_bp = Blueprint("external_search", __name__)

dotenv.load_dotenv()

BASE_URL = "https://api.edamam.com"
app_id = os.environ['APPLICATION_ID']
app_key = os.environ['APPLICATION_KEY']


@external_search_bp.route('/external_search')
@logged_in
def externach_search_page(user_id):
    """Page with external API search for a product"""
    return render_template('external_search.html')


@external_search_bp.route('/search/external/<name>')
@logged_in
def search_via_external_api(name, user_id):
    params = {'app_id': app_id, 'app_key': app_key,
              'ingr': name, 'nutrition-type': 'logging'}
    request = requests.get(
        'https://api.edamam.com/api/food-database/v2/parser', params=params)
    response = request.json()
    return jsonify(response)


@external_search_bp.route('/api/categories')
@logged_in
def get_all_product_categories(user_id):
    """To get a list of all available product categories"""
    categories = services.external_search.get_product_categories()
    return jsonify(categories)


@external_search_bp.route('/api/products', methods=['POST'])
@logged_in
def adding_new_product(user_id):
    """To add a new product"""
    product_name = request.json['product']
    category_id = request.json['category_id']
    find_product = services.external_search.find_product(
        product_name, category_id)

    if len(find_product) != 0:
        return (jsonify(message='already exists'))

    new_product = services.external_search.add_product(
        product_name, category_id)
    return (new_product, 201)
