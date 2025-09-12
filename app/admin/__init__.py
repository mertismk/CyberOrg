from flask import Blueprint

bp = Blueprint('admin', __name__)

# Импортируем маршруты, чтобы они зарегистрировались в blueprint
from . import routes
