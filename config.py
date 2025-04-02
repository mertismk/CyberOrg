import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_key_for_cyberorg")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///cyberorg.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False 