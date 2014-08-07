# Flask-Blog

Simple blog with an administrator area created with the purpose of learning
[Flask](http://flask.pocoo.org) and Python. The design is prototyped with
[Bootstrap](http://twitter.github.io/bootstrap).

Some future plans involves tags, roles, public author profile, syntax
highlighting for code snippets, comment system, image upload and more tests.

## License
Licensed under GNU GPL v3.0.

## Install

### OS Packages

You will at least need the python development package though there might be
more packages required depending on your setup.

    $ sudo apt-get install python-dev

### Python Packages

Click [here](http://www.pip-installer.org/en/latest/index.html) for more
information on using pip and installing a virtual environment.

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt

### Initialize

The following command will create all tables and fill the database with dummy
blog posts.

    (venv)$ python manage.py init

Additional commands are

    dropdb (Drop all tables in database)
    initdb (Create all tables)
    filldb (Fill database with dummy blog posts)

## Test

### Run all tests
    (venv)$ nosetests

### Run a specific test
    (venv)$ nosetests tests/test_filters.py:TestFilters.test_pluralize

## Run

    (venv)$ python manage.py runserver

Login with **admin** as default username and password. Just add /admin to the
url or press the login icon at the top of the page.
