"""Gunicorn *development* config file"""

# Falcon WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "routes:app"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 3
# The socket to bind
bind = "0.0.0.0:5000"
# Restart workers when code changes (development only!)
reload = True
# Write access and error info to /var/log
accesslog = errorlog = "/var/log/gunicorn/dev.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
# pidfile = "/var/run/gunicorn/dev.pid" Only necessary when not running as a service
# We will systemd to monitor the process, so no need for a daemon
daemon = False
