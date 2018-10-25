from flask import Blueprint

api = Blueprint('api', __name__)

from . import student, classes, test, user