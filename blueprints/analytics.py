from flask import Blueprint, Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
import requests
import dotenv
import os
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
import plotly.express as px
from datetime import datetime, date, timedelta
from functools import wraps
import services
from app_util.logged import logged_in

analytics_bp = Blueprint("analytics", __name__)


##### Analytics ####
@analytics_bp.route('/analytics')
@logged_in
def history_analytics_page(user_id):
    """To display charts and history of grocery spending"""

    check_user = services.analytics.check_user_has_data(user_id)
    if len(check_user) == 0:
        flash("The total price and checked flag need to be updated for at least one grocery list/product to view this page", "danger")
        return redirect('/')

    date = datetime.today() - timedelta(days=31)
    print(date, "date")
    fig = services.analytics.total_price_to_date(date, user_id)
    render_template_string(fig.to_html())
    f1 = fig.to_html()

    fig2 = services.analytics.total_number_items_bought(user_id, date)
    render_template_string(fig2.to_html())
    f2 = fig2.to_html()

    fig3 = services.analytics.total_number_items_bought_vs_price_for_date(
        user_id, date)
    render_template_string(fig3.to_html())
    f3 = fig3.to_html()

    fig4 = services.analytics.total_products_per_category(user_id, date)
    render_template_string(fig4.to_html())
    f4 = fig4.to_html()

    fig5 = services.analytics.most_expensive_groceries(user_id)
    render_template_string(fig5.to_html())
    f5 = fig5.to_html()
    return render_template('analytics.html',  f1=f1, f2=f2, f3=f3, f4=f4, f5=f5)
