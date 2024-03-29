from flask import Blueprint, Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
import requests
import dotenv
import os
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from functools import wraps
import services
from app_util.logged import logged_in


lists_bp = Blueprint("lists", __name__)


#### LISTS ROUTES ####


@lists_bp.route('/lists')
@logged_in
def show_lists_page(user_id):
    """To show all lists where the user can add/edit/delete them"""
    return render_template('lists.html')


@lists_bp.route('/api/list/products/<date>')
@logged_in
def get_list_products(date, user_id):
    """To get all products of the user's grocery list"""
    response = services.lists.get_user_list_products(session['username'], date)
    return response


@lists_bp.route('/api/list/products', methods=['POST'])
@logged_in
def add_new_product_to_list(user_id):
    """To add a new product to grocery list"""
    date = request.json['date']
    product_id = request.json['product_id']
    quantity = request.json.get('quantity')
    response = services.lists.add_new_product(
        session['username'], date, product_id, quantity)
    return response, 201


@lists_bp.route('/api/list/products/<int:id>', methods=['DELETE'])
@logged_in
def delete_product(id, user_id):
    """To delete a product from the grocery list"""
    list_product = services.lists.delete_list_product(id)
    return jsonify(message='deleted')


@lists_bp.route('/api/list/products/<int:id>', methods=["PATCH"])
@logged_in
def update_quantity_product(id, user_id):
    """To update quantity of item from don't forget list"""
    quantity = request.json.get('quantity')
    bought = request.json.get('bought')
    response = services.lists.update_product_quantity(id, quantity, bought)
    return response, 201


@lists_bp.route('/api/list/products/reminders', methods=['POST'])
@logged_in
def add_reminders_to_the_list(user_id):
    """To update the grocery list with saved reminders. Once the list is updated the reminders are deleted"""
    date = request.json['date']
    reminders = services.lists.compare_reminders_with_current_list(
        session['username'], date)
    if not reminders:
        return jsonify(message="No reminders have been found")
    return (jsonify(message="The reminders have been added"), 201)


@lists_bp.route('/api/list', methods=['PATCH'])
@logged_in
def update_grocery_list(user_id):
    """To update grocery list"""

    date = request.json['date']
    price = request.json['price']
    response = services.lists.update_price_grocery_list(
        session['username'], date, price)
    return response
