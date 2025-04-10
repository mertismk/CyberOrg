from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db, super_admin_required # Импортируем db и декоратор
from app.models import User, ROLE_EDUCATIONAL_CURATOR, ROLE_ORGANIZATIONAL_CURATOR, ROLE_ADMIN, ROLE_SUPER_ADMIN
from app.users import bp # Импортируем текущий blueprint

# Список допустимых ролей для валидации
VALID_ROLES = [ROLE_EDUCATIONAL_CURATOR, ROLE_ORGANIZATIONAL_CURATOR, ROLE_ADMIN, ROLE_SUPER_ADMIN]


@bp.route("/") # Базовый URL будет /users (задается при регистрации blueprint)
@super_admin_required
def users_list():
    users = User.query.all()
    # Шаблон ищем в users/templates/users/users.html
    return render_template("users/users.html", users=users)


@bp.route("/new", methods=["GET", "POST"])
@super_admin_required
def user_new():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        first_name = request.form.get("first_name") # Получаем имя
        last_name = request.form.get("last_name")   # Получаем фамилию

        # Проверка, что пользователь с таким именем не существует
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует.", "danger")
            # Используем .user_new для ссылки внутри blueprint
            return redirect(url_for("users.user_new"))

        # Проверка валидности роли
        if role not in VALID_ROLES:
            flash("Выбрана недопустимая роль.", "danger")
            # Возвращаем форму с ошибкой, не перенаправляем
            return render_template("users/user_form.html"), 400 # Можно указать код ошибки

        # TODO: Добавить first_name, last_name? - Теперь добавлено
        user = User(
            username=username,
            role=role,
            first_name=first_name, # Сохраняем имя
            last_name=last_name    # Сохраняем фамилию
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Пользователь успешно создан!", "success")
        # Используем .users_list для ссылки внутри blueprint
        return redirect(url_for("users.users_list"))

    # Шаблон ищем в users/templates/users/user_form.html
    return render_template("users/user_form.html")


@bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@super_admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        role = request.form.get("role")
        password = request.form.get("password")
        # TODO: Обновление first_name, last_name? - Добавляем получение
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # Проверка валидности роли
        if role not in VALID_ROLES:
            flash("Выбрана недопустимая роль.", "danger")
            # Возвращаем форму редактирования с ошибкой
            return render_template("users/user_form.html", user=user), 400

        user.role = role
        # Сохраняем имя и фамилию
        user.first_name = first_name
        user.last_name = last_name
        if password:
            user.set_password(password)

        db.session.commit()

        flash("Данные пользователя обновлены!", "success")
        return redirect(url_for("users.users_list"))

    # Шаблон ищем в users/templates/users/user_form.html
    return render_template("users/user_form.html", user=user)


@bp.route("/<int:user_id>/confirm_delete", methods=["GET"])
@super_admin_required
def confirm_user_delete(user_id):
    # Нельзя удалить самого себя
    if user_id == current_user.id:
        flash("Вы не можете удалить свой собственный аккаунт.", "danger")
        return redirect(url_for("users.users_list"))
        
    user = User.query.get_or_404(user_id)
    # Отображаем страницу подтверждения
    return render_template("users/confirm_delete.html", user=user)


@bp.route("/<int:user_id>/delete", methods=["POST"])
@super_admin_required
def user_delete(user_id):
    # Нельзя удалить самого себя
    if user_id == current_user.id:
        flash("Вы не можете удалить свой собственный аккаунт.", "danger")
        return redirect(url_for("users.users_list"))
        
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f"Пользователь '{user.username}' успешно удален.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении пользователя: {str(e)}", "danger")
        
    return redirect(url_for("users.users_list"))
