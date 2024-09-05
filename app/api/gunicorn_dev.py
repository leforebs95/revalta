"""Gunicorn *development* config file"""

# Falcon WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "run:flask_app"
# The granularity of Error log outputs
loglevel = "info"
# The number of worker processes for handling requests
workers = 3
threads = 12
# The socket to bind
bind = "0.0.0.0:5000"
# Restart workers when code changes (development only!)
reload = True
# Redirect stdout/stderr to log file
capture_output = False
# Write access and error info to /var/log
# accesslog = errorlog = "/var/log/gunicorn/dev.log"
