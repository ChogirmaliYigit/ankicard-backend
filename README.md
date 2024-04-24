# A minimal django project template


# Overview

Welcome to our Django Project Template, a meticulously crafted template aimed at expediting the project setup process and establishing a robust foundation for your web applications. This template is thoughtfully designed to empower you with essential features and configurations, allowing you to jumpstart your projects effortlessly and save valuable time.

## Key Features:

1.  **Admin Panel Integration:**
    - Harness the power of a sophisticated admin panel with [django-unfold](http://github.com/unfoldadmin/django-unfold/). Manage your application's data seamlessly and gain insights into your database with ease.

2.  **Environment Variables Simplified:**
    - Effortlessly configure your application using environment variables. This streamlined approach ensures flexibility and enhances security by separating configuration from code.

3.  **Code Quality Assurance:**
    - Elevate your code quality with the inclusion of PyLint and pre-commit configurations. PyLint enforces coding standards and identifies potential issues, while pre-commit hooks run checks before each commit, ensuring a clean and consistent codebase.

## Why Choose our Django Project Template?

- **Speed and Efficiency:**
  - Say goodbye to tedious setup procedures. With our template, you can initiate projects quickly, focusing on building features rather than dealing with complex configurations.

- **Best Practices Out of the Box:**
  - Benefit from industry best practices integrated into the template. We've carefully selected tools and configurations to ensure your project adheres to high coding standards and practices.

- **Community-Backed Components:**
  - Leverage the capabilities of [django-unfold](http://github.com/unfoldadmin/django-unfold/) and other community-backed components. Join a community of developers contributing to the growth and improvement of these tools.

## Getting Started:

### **Installation:**
- _Clone repository_ `git clone https://github.com/ChogirmaliYigit/django-template.git`

### **Configuration:**
- _Run_ `bash set_pre_commit.sh` to set the pre-commit.
- _Run_ `cp .env.example .env`. Then configure the `.env` file's constants.
- Create an environment using command `python -m venv venv`
- Install requirements using command `pip install -r requirements.txt`
- After configure your database, you can run `python manage.py makemigrations` and `python manage.py migrate`.
- Also run the commands: `python manage.py collectstatic` and `python manage.py compilemessages`
- Create a superuser using the command `python manage.py createsuperuser` and start development!

### **App creation:**
- If you want to create an app, you need to go to the `apps` directory using command `cd apps/` and run this command: `python ../manage.py startapp <app_name>`
