from flask import Blueprint

user_management = Blueprint('user_management', __name__)

from . import routes
