from flask import Blueprint

# Указываем папку с шаблонами для этого Blueprint
bp = Blueprint('users', __name__, template_folder='templates')

from app.users import routes # Импортируем маршруты
