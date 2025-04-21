import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class Config:
    # Используем переменную окружения SECRET_KEY, без дефолтного значения в коде
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("Отсутствует SECRET_KEY в переменных окружения")

    # Указываем путь к базе данных, по умолчанию в директории instance
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///cyberorg.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
