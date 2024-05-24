from flask import Blueprint

forecasting = Blueprint('forecasting', __name__)

from . import routes
