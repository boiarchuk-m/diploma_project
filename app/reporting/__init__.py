from flask import Blueprint

reporting = Blueprint('reporting', __name__)

from . import routes
