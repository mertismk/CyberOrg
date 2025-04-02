from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.auth import bp
from app.models import db, User # Импортируем db и User из app.models


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Перенаправляем на главную страницу (предполагаем, что она будет в 'main' blueprint)
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            # Проверяем, не является ли пароль стандартным
            if user.check_password("123456"):
                flash(
                    "Вы используете стандартный пароль. Пожалуйста, измените его в целях безопасности.",
                    "warning",
                )
                return redirect(url_for('auth.profile')) # Используем имя blueprint

            next_page = request.args.get('next')
            # Проверка безопасности: убеждаемся, что next_page ведет на тот же сайт
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index') # По умолчанию на главную
            return redirect(next_page)
        else:
            flash("Неверное имя пользователя или пароль.", "danger")

    # Шаблон ищем в папке templates модуля auth
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из системы.", "success")
    return redirect(url_for('auth.login')) # Перенаправляем на страницу логина


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash("Текущий пароль указан неверно.", "danger")
        elif new_password != confirm_password:
            flash("Новый пароль и подтверждение не совпадают.", "danger")
        elif len(new_password) < 6:
            flash("Новый пароль должен содержать не менее 6 символов.", "danger")
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash("Пароль успешно изменен!", "success")
            # Перенаправляем на главную страницу
            return redirect(url_for('main.index'))

    # Проверяем, использует ли пользователь стандартный пароль
    is_default_password = current_user.check_password("123456")

    # Шаблон ищем в папке templates модуля auth
    return render_template('auth/profile.html', is_default_password=is_default_password)

# Вспомогательная функция для проверки URL (если не используется в других местах)
from urllib.parse import urlparse, urljoin
from flask import request

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

# Альтернативная реализация проверки next_page в login (можно использовать is_safe_url)
# if not next_page or not is_safe_url(next_page):
#     next_page = url_for('main.index')
