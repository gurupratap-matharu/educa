# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html

import multiprocessing

# restart workers after so many requests with some variability
max_requests = 1000
max_requests_jitter = 50


bind = "unix:/run/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
# Access log - records incoming HTTP requests
# accesslog = "/var/log/gunicorn_access.log"

# Error log - records Gunicorn server errors
# errorlog = "/var/log/gunicorn_error.log"
log_file = "-"


# Whether to send Django output to the error log
capture_output = True
# How verbose the Gunicorn error logs should be
loglevel = "info"
enable_stdio_inheritance = True
