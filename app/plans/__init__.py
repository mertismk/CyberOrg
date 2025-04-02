from flask import Blueprint

bp = Blueprint('plans', __name__, template_folder='templates', url_prefix='/plan') # Сразу задаем префикс

from app.plans import routes
