from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db, super_admin_required # Импортируем db и декоратор
from app.models import User # Импортируем модель User
from app.users import bp # Импортируем текущий blueprint


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

        # Проверка, что пользователь с таким именем не существует
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует.", "danger")
            # Используем .user_new для ссылки внутри blueprint
            return redirect(url_for("users.user_new"))

        # TODO: Добавить first_name, last_name?
        user = User(username=username, role=role)
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
        # TODO: Обновление first_name, last_name?

        user.role = role
        if password:
            user.set_password(password)

        db.session.commit()

        flash("Данные пользователя обновлены!", "success")
        return redirect(url_for("users.users_list"))

    # Шаблон ищем в users/templates/users/user_form.html
    return render_template("users/user_form.html", user=user)
