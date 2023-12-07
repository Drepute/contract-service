bind = "{}:{}".format("0.0.0.0", 5000)
wsgi_app = "app:app"

timeout = 120
workers = 2
threads = 4
worker_class = "gthread"
keepalive = 75

daemon = False

errorlog = "-"
loglevel = "debug"
accesslog = "-"
