"""Gunicorn *development* config file"""

import os
import secrets

# Global variable to store the secret key
_secret_key = None


def on_starting(server):
    """
    Generate a secret key when the master process starts.
    This runs before any workers are forked.
    """
    global _secret_key
    # Generate a secure random key
    _secret_key = secrets.token_hex(32)


def post_fork(server, worker):
    """
    Set the secret key in each worker process after forking.
    This ensures all workers have the same key.
    """
    # Make the secret key available to the application
    os.environ["SECRET_KEY"] = _secret_key


# Falcon WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "run:app"
# The granularity of Error log outputs
loglevel = "info"
# The number of worker processes for handling requests
workers = 4
threads = 16
# The socket to bind
bind = "0.0.0.0:5003"
# Restart workers when code changes (development only!)
reload = True
# Redirect stdout/stderr to log file
capture_output = False
