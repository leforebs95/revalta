from flask import Blueprint

auth = Blueprint("session", __name__)

from . import routes
