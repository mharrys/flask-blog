# Flask-Blog

Project still in early stages. 

The application now features a [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) API backend for all administration tasks which is controlled by the administration application written in Javascript with [Backbone.Marionette](http://marionettejs.com), [RequireJS](http://requirejs.org) and [Moment.js](http://momentjs.com). The visual is prototyped with [Bootstrap](http://twitter.github.io/bootstrap).

The authorization is for now being done with HTTP Basic and should **only** be used over SSL. Every request sent to the server API requires valid authorization header. The [Backbone.BasicAuth](https://github.com/fiznool/backbone.basicauth) library is used to help set this header, however this project is using a [fork](https://github.com/mharrys/backbone.basicauth) for now.

The blog is still written like any traditional Flask application without any need for Javascript. The visual is written from the ground up with [Sass](http://sass-lang.com) and [Susy](http://susy.oddbird.net).

Some future plans involves tags, admin roles, test for views, public author profile, syntax highlighting for code snippets, better comment system and image upload.

Its known that the dates are displayed wrong in the administration application for SQLite.

## Install

### Download

    $ git clone git://github.com/mharrys/flask-blog.git
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
    (venv)$ nosetests tests/test_filters.py:TestFilters.test_pluralize

## Run

    (venv)$ python manage.py runserver

Login with **admin** as default username and password.
