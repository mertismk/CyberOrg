from flask import Blueprint

# Указываем общую папку шаблонов, т.к. основные шаблоны будут лежать там
bp = Blueprint('main', __name__, template_folder='../templates')

from app.main import routes # Импортируем маршруты
