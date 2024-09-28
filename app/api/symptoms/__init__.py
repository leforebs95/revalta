from flask import Blueprint

symptoms = Blueprint("symptoms", __name__)

from . import routes
