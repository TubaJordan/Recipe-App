# Recipe App

## Overview

The Recipe App is a fully functional web application designed to allow users to create, read, and modify recipes, as well as search for recipes based on ingredients. Built with Python and Django, this app demonstrates the capabilities of modern web application development, including user authentication, dynamic content creation, and data visualization. The project aims to showcase the developer's understanding of the Django web framework and their ability to develop a comprehensive web application.

## Technical Requirements

- Python 3.6+ and Django 3 compatibility.
- Exception handling with user-friendly error messages.
- PostgreSQL for production and SQLite for development database connectivity.
- Easy-to-use interface with simple forms and clear instructions.
- Code documentation and automated tests hosted on GitHub.
- Includes a "requirements.txt" for easy project setup.

## Key Features

- User authentication, login, and logout.
- Recipe search by ingredients.
- Automatic difficulty rating for each recipe.
- Error handling on user input.
- Detailed recipe information on demand.
- User recipe submissions with SQLite database integration.
- Django Admin dashboard for database management.
- Statistical analysis and visualization of recipe trends.

## User Goals

- To create and modify recipes with ease, including details such as ingredients, cooking time, and an automated difficulty level.
- To search for recipes by ingredient.
- To engage with a community of users through recipe sharing and feedback.

## Setup and Installation

1. **Clone the repository:**

```bash
git clone [repository URL]
cd recipe-app
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Setup Database:**

- Adjust the `DATABASES` configuration in `settings.py` for PostgreSQL and SQLite as per your development and production environments.

4. **Run Migrations:**

```bash
python manage.py migrate
```

5. **Create Superuser for Admin Access:**

```bash
python manage.py createsuperuser
```

6. **Run the Development Server:**

```bash
python manage.py runserver
```

- Visit `http://127.0.0.1:8000` in your browser to view the app.
