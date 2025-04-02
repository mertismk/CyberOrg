import os
from flask import Flask, request, redirect, url_for, flash, render_template
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from datetime import datetime, timedelta
from functools import wraps
import click
from flask.cli import with_appcontext

from config import Config
from .models import db, User  # Импортируем db и User из models

# Инициализация расширений без привязки к приложению
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Указываем Blueprint для login_view
login_manager.login_message = "Пожалуйста, войдите для доступа к этой странице."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Декораторы для проверки прав доступа
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("У вас нет прав доступа к этой странице.", "danger")
            return redirect(url_for("main.index")) # Перенаправляем на главную страницу (будет в main blueprint)
        return f(*args, **kwargs)

    return decorated_function


def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_super_admin:
            flash("У вас нет прав доступа к этой странице.", "danger")
            return redirect(url_for("main.index")) # Перенаправляем на главную страницу
        return f(*args, **kwargs)

    return decorated_function


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Регистрация Blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Регистрация других Blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from .students import bp as students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    from .webinars import bp as webinars_bp
    app.register_blueprint(webinars_bp, url_prefix='/webinars')

    from .plans import bp as plans_bp
    app.register_blueprint(plans_bp) # Префикс /plan уже задан в Blueprint

    # Обновление времени последнего доступа
    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_login = datetime.utcnow()
            db.session.commit()

    # Регистрация фильтров Jinja2
    @app.template_filter("yesno")
    def yesno_filter(value):
        return "Да" if value else "Нет"

    @app.template_filter("moscow_time")
    def moscow_time_filter(date):
        if date is None:
            return "Не указано"
        if isinstance(date, datetime):
            moscow_time = date + timedelta(hours=3)
            return moscow_time.strftime("%d.%m.%Y %H:%M (МСК)")
        else:
            return date.strftime("%d.%m.%Y") # Только дата

    @app.template_filter("webinar_cover_exists")
    def webinar_cover_exists(webinar_id):
        # Путь теперь относительно папки static внутри app
        cover_path = os.path.join(app.static_folder, "covers", f"{webinar_id}.png")
        return os.path.exists(cover_path)

    # Регистрация обработчиков ошибок
    @app.errorhandler(404)
    def page_not_found(e):
        # Предполагаем, что шаблон 404.html будет в папке templates
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        # Предполагаем, что шаблон 403.html будет в папке templates
        return render_template("403.html"), 403

    return app
