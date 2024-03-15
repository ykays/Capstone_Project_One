from models import User, db, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from app import app
from csv import DictReader

#Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()


    # Add new users
    test_user = User.signup(username = "test_user" , password="test_user_password!9" , email="test_user@gmail.com")
    # Add new objects to the session
    db.session.add(test_user)
 

    # Commit changes
    db.session.commit()

    # Add List Templates
    temp1 = ListTemplate(template_name ="test_user_template", user_id = 1)

    db.session.add(temp1)
    # Commit changes
    db.session.commit()

    # Add Product Categories
    with open('generate/product_categories.csv') as categories:
        db.session.bulk_insert_mappings(ProductCategory, DictReader(categories))
    
    db.session.commit()

    # Add Products
    with open('generate/products.csv') as products:
        db.session.bulk_insert_mappings(Product, DictReader(products))
    
    db.session.commit()

    # Add template products for test user
    tp1 = TemplateProduct(template_id=1, product_id=1)
    tp2= TemplateProduct(template_id=1, product_id=2)
    tp3 = TemplateProduct(template_id=1, product_id=3)
    tp4 = TemplateProduct(template_id=1, product_id=4)
    tp5 = TemplateProduct(template_id=1, product_id=5)
    tp6 = TemplateProduct(template_id=1, product_id=10)
    tp7 = TemplateProduct(template_id=1, product_id=11)
    tp8 = TemplateProduct(template_id=1, product_id=12)
    tp9 = TemplateProduct(template_id=1, product_id=20)
    tp10 = TemplateProduct(template_id=1, product_id=21)
    tp11 = TemplateProduct(template_id=1, product_id=32)

    db.session.add_all([tp1, tp2, tp3, tp4, tp5, tp6, tp7, tp8, tp9, tp10, tp11])
    db.session.commit()

    # Add grocery list for test user
    gl1 = GroceryList(user_id=1, date='2024-03-14', template_id=1)
    gl2 = GroceryList(user_id=1, date='2024-03-05', template_id=1, total_price= 105.68)
    gl3 = GroceryList(user_id=1, date='2024-03-02', template_id=1, total_price= 113.90)
    gl4 = GroceryList(user_id=1, date='2024-02-28', template_id=1, total_price= 125.97)
    gl5 = GroceryList(user_id=1, date='2024-02-18', template_id=1, total_price= 80.68)
    gl6 = GroceryList(user_id=1, date='2024-03-10', template_id=1, total_price= 98.40)
    gl7 = GroceryList(user_id=1, date='2024-02-10', template_id=1, total_price= 150.31)
    gl8 = GroceryList(user_id=1, date='2024-02-05', template_id=1, total_price= 140.90)
    gl9 = GroceryList(user_id=1, date='2024-02-01', template_id=1, total_price= 99.40)
    gl10 = GroceryList(user_id=1, date='2024-01-20', template_id=1, total_price= 96.93)
    gl11 = GroceryList(user_id=1, date='2024-01-15', template_id=1, total_price= 123.45)

    db.session.add_all([gl1, gl2, gl3, gl4, gl5, gl6, gl7, gl8, gl9, gl10, gl11])
    db.session.commit()

      # Add Grocery List Products
    with open('generate/grocery_products.csv') as products:
        raw_products = list(DictReader(products))
    transformed_products = []
    for product in raw_products:
        transformed_products.append({**product,"bought":product['bought'].lower()=="true"})

    db.session.bulk_insert_mappings(GroceryListProducts, transformed_products)
    
    db.session.commit()

    # Add don't forget items
    r1 = Reminder(user_id=1, product_id=198, quantity=1)
    r2 = Reminder(user_id=1, product_id=8, quantity=1)
    r3 = Reminder(user_id=1, product_id=9, quantity=1)
    
    db.session.add_all([r1, r2, r3])
    db.session.commit()