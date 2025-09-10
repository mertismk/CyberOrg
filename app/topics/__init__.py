from flask import Blueprint

bp = Blueprint('topics', __name__, template_folder='templates')

from app.topics import routes
