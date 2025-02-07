from flask import Blueprint

ocr = Blueprint("ocr", __name__)

from . import routes
