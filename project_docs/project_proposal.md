# Project Proposal - _EASY GROCERY app_

Use this template to help get you started right away! Once the proposal is complete, please let your mentor know that this is ready to be reviewed.

## Get Started

|            | Description                                                                                                                                                                                                                                                                                                                                              | Fill in                                                                                                                                                            |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tech Stack | What tech stack will you use for your final project? It is recommended to use the following technologies in this project: Python/Flask, PostgreSQL, SQLAlchemy, Heroku, Jinja, RESTful APIs, JavaScript, HTML, CSS. Depending on your idea, you might end up using WTForms and other technologies discussed in the course.                               | Python/Flask, PostgreSQL, SQLAlchemy, Jinja, RESTful APIs, JS, HTML, CSS, WTForms, matplotlib (or other library to create charts)                                  |
| Type       | Will this be a website? A mobile app? Something else?                                                                                                                                                                                                                                                                                                    | Website, and mobile for Shopping (stretch goal - both web and mobile)                                                                                              |
| Goal       | What goal will your project be designed to achieve?                                                                                                                                                                                                                                                                                                      | The app should make the grocery simpler, more effective, and fun!                                                                                                  |
| Users      | What kind of users will visit your app? In other words, what is the demographic of your users?                                                                                                                                                                                                                                                           | Users doing grocery shopping - age 18-60                                                                                                                           |
| Data       | What data do you plan on using? How are you planning on collecting your data? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. You are welcome to create your own API and populate it with data. If you are using a Python/Flask stack, you are required to create your own API. | Data about users/grocery templates/grocery lists/categories will be stored in DB; External API to get new products; RESTful API with get/post/patch/delete routes; |

# High level overview - Easy Shopping

1. User can register/log in.
2. User can create a grocery list template that will be stored in DB.
3. User can update a grocery list template (edit existing record, delete existing record, add a new record to the list).
4. User can create the grocery list by retrieving the saved template and add the grocery date, make changes to the retrieved list (the app will ask if the made changes should also be applied to the template). The grocery list will be stored.
5. User will be able to search for new products. When the product is selected and added to the grocery or template list, the user will be asked to select the category of the product (if not already assigned), ie. produce, meat, frozen food.
6. User will be able to use the grocery list and check out individual items as shopping progresses. The grocery list will be organized in the category buckets (produce, bakery, canned food, meat, etc). Nice to have - start and end time of grocery shoppging that will be used in the charts to show how much time was spent on each grocery shopping.
7. User will be able to input the individual price item and/or total price. This will update the grocery list for that date. It will be used in the charts to show how much money they spend on the grocery in total and/or individual items.

// External API:

- API to get find a product (ideally, with autocomplete)

// Database (tables):

- Users
- Grocery Templates (join with users table)
- Grocery List with Date (join with users table)
- Static table of the product categories

// RESTful APIs:

- Register User
- Login User
- Add Template
- Edit Template
- Delete Template
- Retrieve the Grocery List
- Edit Grocery List
- Delete Grocery List
- Update Grocery List (check out items)
- View history of the groceries

App sections:
<img width="2001" alt="Easy Grocery" src="https://github.com/hatchways-community/capstone-project-one-c957d379ad674e81bcde8ab0c2be2359/assets/63420594/eff24578-ca80-4a4e-9857-3252de35e44c">

# Breaking down your project (still to be filled once approved by my mentor)

When planning your project, break down your project into smaller tasks, knowing that you may not know everything in advance and that these details might change later. Some common tasks might include:

- Determining the database schema
- Sourcing your data
- Determining user flow(s)
- Setting up the backend and database
- Setting up the frontend
- What functionality will your app include?
  - User login and sign up
  - Uploading a user profile picture

Here are a few examples to get you started with. During the proposal stage, you just need to create the tasks. Description and details can be edited at a later time. In addition, more tasks can be added in at a later time.

| Task Name                   | Description                                                                                                   | Example                                                           |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Design Database schema      | Determine the models and database schema required for your project.                                           | [Link](https://github.com/hatchways/sb-capstone-example/issues/1) |
| Source Your Data            | Determine where your data will come from. You may choose to use an existing API or create your own.           | [Link](https://github.com/hatchways/sb-capstone-example/issues/2) |
| User Flows                  | Determine user flow(s) - think about what you want a user’s experience to be like as they navigate your site. | [Link](https://github.com/hatchways/sb-capstone-example/issues/3) |
| Set up backend and database | Configure the environmental variables on your framework of choice for development and set up database.        | [Link](https://github.com/hatchways/sb-capstone-example/issues/4) |
| Set up frontend             | Set up frontend framework of choice and link it to the backend with a simple API call for example.            | [Link](https://github.com/hatchways/sb-capstone-example/issues/5) |
| User Authentication         | Fullstack feature - ability to authenticate (login and sign up) as a user                                     | [Link](https://github.com/hatchways/sb-capstone-example/issues/6) |

## Labeling

Labeling is a great way to separate out your tasks and to track progress. Here’s an [example](https://github.com/hatchways/sb-capstone-example/issues) of a list of issues that have labels associated.

| Label Type    | Description                                                                                                                                                                                                                                                                                                                     | Example                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Difficulty    | Estimating the difficulty level will be helpful to determine if the project is unique and ready to be showcased as part of your portfolio - having a mix of task difficultlies will be essential.                                                                                                                               | Easy, Medium, Hard           |
| Type          | If a frontend/backend task is large at scale (for example: more than 100 additional lines or changes), it might be a good idea to separate these tasks out into their own individual task. If a feature is smaller at scale (not more than 10 files changed), labeling it as fullstack would be suitable to review all at once. | Frontend, Backend, Fullstack |
| Stretch Goals | You can also label certain tasks as stretch goals - as a nice to have, but not mandatory for completing this project.                                                                                                                                                                                                           | Must Have, Stretch Goal      |
