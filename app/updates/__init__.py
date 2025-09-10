from flask import Blueprint

# Указываем папку с шаблонами для этого Blueprint
bp = Blueprint('updates', __name__, template_folder='templates')

from app.updates import routes  # Импортируем маршруты
