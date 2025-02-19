from flask import Blueprint

vector = Blueprint("vector", __name__)

from . import routes
