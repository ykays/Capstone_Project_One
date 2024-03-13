from models import User, db, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from app import app
from csv import DictReader

#Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()


    # Add new users
    anna = User.signup(username = "anna" , password="anna123" , email="anna123@gmail.com"  )
    mike = User.signup(username = "mike" , password="mike123" , email="mike123@gmail.com" )
    kevin = User.signup(username = "kevin" , password="kevin123" , email="kevin123@gmail.com" )
    # Add new objects to the session
    db.session.add(anna)
    db.session.add(mike)
    db.session.add(kevin)

    # Commit changes
    db.session.commit()

    # Add List Templates
    temp1 = ListTemplate(template_name ="anna_template", user_id = 1)
    temp2 = ListTemplate(template_name ="mike_template", user_id = 2)
    temp3 = ListTemplate(template_name ="kevin_template", user_id = 3)

    db.session.add_all([temp1, temp2, temp3])
    # Commit changes
    db.session.commit()

    with open('generate/product_categories.csv') as categories:
        db.session.bulk_insert_mappings(ProductCategory, DictReader(categories))
    
    db.session.commit()

    with open('generate/products.csv') as products:
        db.session.bulk_insert_mappings(Product, DictReader(products))
    
    db.session.commit()


