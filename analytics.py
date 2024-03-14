from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
import plotly.express as px
import pandas as pd

def setting_date(dates):
   df = pd.DataFrame()
   df['date'] = dates
   df = df.set_index('date')
   return pd.to_datetime(df.index).strftime("%m/%d/%Y")
   
def total_price_to_date(date, user_id):
   price_dates = db.session.query(GroceryList.date, GroceryList.total_price).filter(GroceryList.date > date, GroceryList.user_id == user_id, GroceryList.total_price>0).order_by(GroceryList.date).all();
   data = []
   for item in price_dates:
      data.append(item._asdict()) 

   dates = [item['date'] for item in data] 
   prices =  [item['total_price'] for item in data] 
    
   fig = px.line(x=setting_date(dates), y=prices,markers=True, width=1200, height=400, title="Total price per date",
                 labels={
                     "x": "Date",
                     "y": "Total price",
                     
                 },)

   fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="LightSteelBlue")
   
   return fig

def total_number_items_bought(user_id, date):
   data = db.session.query(GroceryList.date, db.func.count(GroceryListProducts.id).label('count')).join(GroceryListProducts, GroceryList.id == GroceryListProducts.grocery_list_id).filter(GroceryList.user_id == user_id, GroceryList.date > date, GroceryListProducts.bought==True).group_by(GroceryList.date).order_by(GroceryList.date).all();
   
   data_dict = []
   for item in data:
      data_dict.append(item._asdict()) 
    
   dates = [item['date'] for item in data_dict] 
   count =  [item['count'] for item in data_dict]

   fig = px.bar(x=setting_date(dates), 
                y=count, width=1200, height=400,text_auto=True,title="Numbers of items bought per date",
                 labels={
                     "x": "Date",
                     "y": "Number of products",
                     
                 },)

   fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="LightSteelBlue")
   
   return fig

def total_number_items_bought_vs_price_for_date(user_id, date):
   
   data = db.session.query(GroceryList.date, GroceryList.total_price, db.func.count(GroceryListProducts.id).label('count')).join(GroceryListProducts, GroceryList.id == GroceryListProducts.grocery_list_id).filter(GroceryList.user_id == user_id, GroceryList.date> date, GroceryListProducts.bought == True).group_by(GroceryList.date, GroceryList.total_price).order_by(GroceryList.date).all();
   
   data_dict = []
   for item in data:
      data_dict.append(item._asdict()) 
 
   dates = [item['date'] for item in data_dict] 
   count =  [item['count'] for item in data_dict] 
   prices = [item['total_price'] for item in data_dict] 

   fig = px.line(x=setting_date(dates), y=prices, markers=True, width=1200, height=400, title="Total price per date",
                 labels={
                     "x": "Date",
                     "y": "Total price",
                     
                 },)
   
   
   fig.add_bar(x=setting_date(dates), 
                y=count, text=count, name="Number of Products")

   fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="LightSteelBlue")
   
   return fig

def total_products_per_category(user_id,date):
   
   data = db.session.query(GroceryList.date, GroceryList.total_price, ProductCategory.category_name, db.func.count(GroceryListProducts.id).label('count')).join(GroceryListProducts, GroceryList.id == GroceryListProducts.grocery_list_id).join(Product, GroceryListProducts.product_id == Product.id).join(ProductCategory, ProductCategory.id == Product.category_id).filter(GroceryList.user_id == user_id, GroceryList.date> date, GroceryListProducts.bought == True).group_by(GroceryList.date, GroceryList.total_price, ProductCategory.category_name).order_by(GroceryList.date).all();
   
   data_dict = []
   for item in data:
      data_dict.append(item._asdict()) 
   
   dates = [item['date'] for item in data_dict] 
   count =  [item['count'] for item in data_dict] 
   prices = [item['total_price'] for item in data_dict] 
   categories = [item['category_name'] for item in data_dict]

   fig = px.bar(x=setting_date(dates), 
                y=count, 
                color=categories, 
                width=1200, height=400,title="Numbers of items bought of each category per date",
                 labels={
                     "x": "Date",
                     "y": "Number of products",
                     
                 },)

   fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="LightSteelBlue")
   
   return fig

def most_expensive_groceries(user_id):
   subquery = db.session.query(GroceryList.date).filter(GroceryList.total_price>0).order_by(GroceryList.total_price.desc()).limit(10).subquery();
   data = db.session.query(GroceryList.date, GroceryList.total_price, db.func.count(GroceryListProducts.id).label('count')).join(GroceryListProducts, GroceryList.id == GroceryListProducts.grocery_list_id).filter(GroceryList.user_id == user_id, GroceryListProducts.bought == True, GroceryList.date.in_(subquery)).group_by(GroceryList.date, GroceryList.total_price).order_by(GroceryList.date).all(); 
   data_dict = []
   for item in data:
      data_dict.append(item._asdict()) 
   
   dates = [item['date'] for item in data_dict] 
   count =  [item['count'] for item in data_dict] 
   prices = [item['total_price'] for item in data_dict] 

   fig = px.line(x=setting_date(dates), y=prices, markers=True, width=1200, height=400, title="Total price per date",
                 labels={
                     "x": "Date",
                     "y": "Total price",
                     
                 },)
   
   
   fig.add_bar(x=setting_date(dates), 
                y=count, text=count, name="Number of Products")

   fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="LightSteelBlue")
   
   return fig