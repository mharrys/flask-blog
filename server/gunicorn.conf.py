import multiprocessing

log = '/var/log/gunicorn/flask-blog.%s.log'
accesslog = log % 'access'
errorlog = log % 'error'

bind = '127.0.0.1:8005'
workers = multiprocessing.cpu_count() * 2 + 1
