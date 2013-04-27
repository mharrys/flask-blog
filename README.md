# Flask-Blog

Project still in early stages.

## Install
    git clone https://github.com/mharrys/flask-blog.git
    cd flask-blog
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py init

## Test

### Run all tests
    nosetests
    
### Run a specific test (Example)
    nosetests tests/test_models.py:TestPost.test_filter_by_oldest

## Run
    python manage.py runserver

Login with **admin** as default username and password.

## Screenshot
A taste of the current frontend design.
![Scrot](http://i.imgur.com/GEY4Fm5.png)

A taste of the current admin design.
![Scrot-Admin](http://i.imgur.com/dxekGka.png)
