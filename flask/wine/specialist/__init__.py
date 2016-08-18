from flask import Blueprint

specialist = Blueprint('specialist', __name__)

from . import views