from flask import Blueprint

lab_results = Blueprint("lab_results", __name__)

from . import routes
