import os

# Gunicorn configuration for Render deployment
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
