from flask import Blueprint

waitlist = Blueprint("waitlist", __name__)

from . import routes
