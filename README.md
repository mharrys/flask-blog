# Flask-Blog

Project still in early stages.

## Install (GNU/Linux)

### Download

    $ git clone https://github.com/mharrys/flask-blog.git
    $ cd flask-blog

### Python Packages

Click [here](http://www.pip-installer.org/en/latest/index.html) for more information on using pip and installing a virtual environment.

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt

### Initialize

The following command will create all tables and fill the database with dummy blog posts.

    (venv)$ python manage.py init

Additional commands are

    dropdb (Drop all tables in database)
    initdb (Create all tables)
    filldb (Fill database with dummy blog posts)

## Test

### Run all tests
    (venv)$ nosetests

### Run a specific test
    (venv)$ nosetests tests/test_models.py:TestPost.test_filter_by_oldest

## Run

    (venv)$ python manage.py runserver

Login with **admin** as default username and password.
