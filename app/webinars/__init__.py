from flask import Blueprint

bp = Blueprint('webinars', __name__, template_folder='templates')

from app.webinars import routes
