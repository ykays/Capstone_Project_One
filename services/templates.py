from flask import jsonify
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts

def get_user_id(username):
    user = User.query.filter(User.username == username).first()
    return user.id

def get_user_templates(user_id):
    users_templates = [template.serialize() for template in ListTemplate.query.filter(ListTemplate.user_id == user_id).all()]
    return users_templates

def create_new_template(template_name, user_id):
    new_template = ListTemplate(template_name=template_name, user_id = user_id)
    db.session.add(new_template)
    db.session.commit()
    return new_template.serialize()

def delete_template(id):
    template = ListTemplate.query.get_or_404(id)
    db.session.delete(template)
    db.session.commit()

def get_template_products(id):
    template_products =  []
    all_products = db.session.query(Product.id, Product.product_name, ProductCategory.category_name).join(TemplateProduct).join(ProductCategory).filter(TemplateProduct.template_id==id).all()
    for product in all_products:
      template_products.append(product._asdict())
    return template_products

def delete_template_product(user_id, id):
    template = ListTemplate.query.filter(ListTemplate.user_id == user_id).first()
    template_product = TemplateProduct.query.filter((TemplateProduct.product_id == id) & 
                                                   (TemplateProduct.template_id == template.id)).first()
   
    db.session.delete(template_product)
    db.session.commit()
    return template.id

def add_template_product(user_id, id):
    template = ListTemplate.query.filter(ListTemplate.user_id == user_id).first()
    product_exist_check = TemplateProduct.query.filter((TemplateProduct.template_id == template.id) 
                                                      & (TemplateProduct.product_id == id)).all()
   
    if len(product_exist_check) != 0: 
        return jsonify(message="already exists", template=template.id)
   
    template_product = TemplateProduct(template_id=template.id, product_id=id)
    db.session.add(template_product)
    db.session.commit()
    return (jsonify(message="added", template=template.id),201)





