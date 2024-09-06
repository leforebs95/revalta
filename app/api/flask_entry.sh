#!/bin/sh

FLASK_SECRET_KEY=$(openssl rand -hex 32)
export FLASK_SECRET_KEY

gunicorn --chdir /usr/src/api -c /usr/src/api/gunicorn_dev.py
