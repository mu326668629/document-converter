import multiprocessing

bind = ['0.0.0.0:8200']
workers = multiprocessing.cpu_count() * 2 + 1
logfile = 'logs/gunicorn.log'
timeout = 30
backlog = 2048
graceful_timeout = 30
limit_request_field_size = 8000
preload_app = False
user = None
daemon = True
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None
debug = False
reload = False
