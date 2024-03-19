# Overview


**Welcome to Easy Grocery App!** (URL: https://easy-grocery.onrender.com/)


_Do you usually buy the same things at your grocery store and even though you always forget something?_

<img width="1368" alt="Home Page" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/8f72d787-3472-4320-a2d2-a14fd705e423">


This application allows you to create your own grocery shopping template which will be used to pre-populate a grocery list for a specific date.
<img width="1395" alt="Home Page Sections" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/32040e3a-7071-4aa6-a89b-1c72ce95726e">
After you register in the app, 
you will able to search for any product in the internal Easy Grocery DB (with search enhanced with suggestions) 
as well as using external API (https://api.edamam.com). 

<img width="1403" alt="Registration" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/057e3ffc-234f-4214-af41-1b89ac0cd221">

<img width="1321" alt="Search" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/cfa8a022-f21d-4c44-8f4f-328d0dc1b764">


Each product has an assigned category (which becomes helpful to find a specific store aisle/section while shopping).

<img width="1317" alt="Template" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/37bb4e96-7e49-4f11-bccb-190146c09db7">

Easy Grocery app contains also a "Don't forget" section, where you can quickly add the item/s you don't want to forget next time doing groceries. 
<img width="1336" alt="Dont forget list" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/4ee4ae90-6661-4138-9faa-1e1ccd038f79">


While creating a grocery list, you can add these products and/or any product you didn't have on either template or don't forget list!
The template, grocery, and don't forget lists can be viewed/modified at any time.
<img width="1347" alt="Grocery List" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/24491b0c-e83c-477d-aa87-c81accabf5bd">


Finally, you will be able to use Easy Grocery list during shopping to checkout the items already bought.
<img width="1320" alt="Grocery List checkouts" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/fe172d26-857f-4d4e-9fee-e1f1ca4883bd">

After the shopping is completed, you may input the total price of each grocery (under each grocery list) 
and then view several analytics charts to analyze your spending, number of items bought, etc.

<img width="835" alt="Analytics1" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/b08843aa-33e9-4376-8561-146fef60ab91">
<img width="728" alt="Analytics2" src="https://github.com/ykays/Capstone_Project_One/assets/63420594/b4a65b37-e88c-48a4-a56e-7cbebd125e04">



The technology stack used to create this app:

- JavaScript
- HTML
- CSS (and bootstrap)
- Python
- Flask
- Flask-SQLAlchemy
- Postgresql
- WTForms
- RESTful API
- Plotly
- Render

# Installation

1. Clone locally the repository: git clone git@github.com:ykays/Capstone_Project_One.git
2. Install requirements: pip install requirements.txt
3. Create new DB locally: createdb grocery_db
4. Replace the DB URI with grocery_db in .env: DATABASE = ‘postgresql://grocery_db'
5. Run seed file to create and populate tables: python seed.py
6. To start app: flask run
7. You may use the user that was created by the seed file (username: test_user; password: test_user_password!9) or register with a new username.
8. To run tests: python -m pytest tests/

# Quick folder description:

1. Project docs - contains DB schema, User’s flow diagram, as well as initial project idea and proposal.
2. Generate - contains the CSV files that are loaded during seed process.
3. Static - contains CSS, JS files and logo pics.
4. Templates - contains all HTML files.
5. Services - contains files with transformation/business logic/DB queries. 
6. Blueprints - contains a file with routes/APIs for each module (as extensions to the main app.py file).
7. Tests - all test files for models and view functions. 
8. Other files:
    - app.py - main file with routes 
    - Models.py - all DB Models;
    - forms.py - registration & login forms 
