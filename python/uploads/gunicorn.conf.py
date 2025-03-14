import multiprocessing
import os

# Environment-specific settings
env = os.environ.get("ENVIRONMENT", "development")

# Base configuration
bind = "0.0.0.0:5001"
worker_class = "gevent"  # Using gevent for async support
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120

# Access logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# Process naming
proc_name = "uploads_service"

# SSL (if needed)
keyfile = os.environ.get("SSL_KEYFILE")
certfile = os.environ.get("SSL_CERTFILE")

# Environment-specific configurations
if env == "development":
    reload = True
    workers = 2
    loglevel = "debug"
    
elif env == "staging":
    workers = multiprocessing.cpu_count() + 1
    max_requests = 1000
    max_requests_jitter = 50
    
elif env == "production":
    workers = multiprocessing.cpu_count() * 2 + 1
    max_requests = 2000
    max_requests_jitter = 100
    preload_app = True
    
    # Production logging
    accesslog = "/var/log/gunicorn/access.log"
    errorlog = "/var/log/gunicorn/error.log"
    
# Worker configurations
worker_tmp_dir = "/dev/shm"  # Using shared memory for better performance
worker_connections = 1000
keepalive = 5

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    pass

def on_reload(server):
    """Called before code is reloaded."""
    pass

def when_ready(server):
    """Called just after the server is started."""
    pass

def on_exit(server):
    """Called just before the server exits."""
    pass 