import os
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import joinedload, selectinload

from app import db
from app.models import Webinar, TaskNumber, WebinarComment, User
from app.webinars import bp


@bp.route("/") # Базовый URL /webinars
@login_required
def webinars_list():
    webinars = Webinar.query.options(
        joinedload(Webinar.created_by),
        selectinload(Webinar.comments).joinedload(WebinarComment.user),
        selectinload(Webinar.task_numbers)
    ).order_by(Webinar.date.desc().nullslast(), Webinar.id.desc()).all()
    # Шаблон webinars/templates/webinars/webinars.html
    return render_template("webinars/webinars.html", webinars=webinars)


@bp.route("/import", methods=["GET", "POST"])
@login_required # Возможно, стоит ограничить права до admin_required?
def import_webinars():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Файл не выбран", "danger")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("Файл не выбран", "danger")
            return redirect(request.url)

        if not file.filename.endswith((".xlsx", ".xls")):
            flash("Поддерживаются только Excel файлы (.xlsx, .xls)", "danger")
            return redirect(request.url)

        try:
            df = pd.read_excel(file)
            required_columns = ["название вебинара", "ссылка на вебинар"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                flash(f'Отсутствуют обязательные колонки: {", ".join(missing_columns)}', "danger")
                return redirect(request.url)

            total_rows = len(df)
            imported_count = 0
            errors = []

            for index, row in df.iterrows():
                try:
                    if pd.isna(row["название вебинара"]) or pd.isna(row["ссылка на вебинар"]):
                        errors.append(f"Строка {index + 2}: Отсутствуют обязательные поля")
                        continue

                    # Проверка на дубликат по URL
                    existing_webinar = Webinar.query.filter_by(url=str(row["ссылка на вебинар"])).first()
                    if existing_webinar:
                        # Опционально: можно обновлять существующий вебинар или пропускать
                        errors.append(f"Строка {index + 2}: Вебинар с таким URL уже существует (ID: {existing_webinar.id})")
                        continue

                    webinar = Webinar(
                        title=str(row["название вебинара"]),
                        url=str(row["ссылка на вебинар"]),
                        created_by_id=current_user.id,
                    )

                    if "дата вебинара" in df.columns and not pd.isna(row["дата вебинара"]):
                        try:
                            webinar.date = pd.to_datetime(row["дата вебинара"]).date()
                        except Exception as e:
                            errors.append(f"Строка {index + 2}: Неверный формат даты ({e})")

                    if "номера заданий" in df.columns and not pd.isna(row["номера заданий"]):
                        task_numbers_str = str(row["номера заданий"])
                        try:
                            task_numbers_list = [int(num.strip()) for num in task_numbers_str.split(',') if num.strip().isdigit()]
                            for num in task_numbers_list:
                                task = TaskNumber.query.filter_by(number=num).first()
                                if not task:
                                    # Если задание не найдено, можно его создать или выдать ошибку
                                    # task = TaskNumber(number=num)
                                    # db.session.add(task)
                                    errors.append(f"Строка {index + 2}: Задание с номером {num} не найдено в базе.")
                                    continue # Пропускаем добавление этого номера
                                if task not in webinar.task_numbers:
                                    webinar.task_numbers.append(task)
                        except Exception as e:
                             errors.append(f"Строка {index + 2}: Ошибка обработки номеров заданий ({e})")

                    if "тип решения" in df.columns and not pd.isna(row["тип решения"]):
                        solution_type = str(row["тип решения"]).lower()
                        webinar.is_programming = any(term in solution_type for term in ["прогой", "программирование", "программный"])
                        webinar.is_manual = any(term in solution_type for term in ["руками", "ручное", "ручной"])

                    if "номер дз" in df.columns and not pd.isna(row["номер дз"]):
                        try:
                            webinar.homework_number = int(row["номер дз"])
                        except ValueError:
                            errors.append(f"Строка {index + 2}: Неверный формат номера ДЗ")

                    if "категория" in df.columns and not pd.isna(row["категория"]):
                        try:
                            category_val = int(row["категория"])
                            if category_val in [1, 2, 3]:
                                webinar.category = category_val
                            else:
                                errors.append(f"Строка {index + 2}: Неверное значение категории ({category_val})")
                        except ValueError:
                             errors.append(f"Строка {index + 2}: Неверный формат категории")

                    if "категория курса" in df.columns and not pd.isna(row["категория курса"]):
                        course_category = str(row["категория курса"]).lower().strip() # Добавим strip() на всякий случай

                        # Сначала сбрасываем все флаги
                        webinar.for_beginners = False
                        webinar.for_basic = False
                        webinar.for_advanced = False
                        webinar.for_expert = False
                        webinar.for_mocks = False
                        webinar.for_practice = False
                        webinar.for_minisnap = False

                        # Затем устанавливаем нужный флаг
                        if course_category == "python с нуля":
                            webinar.for_beginners = True
                        elif course_category == "основной курс":
                            webinar.for_basic = True
                        elif course_category == "хард прога":
                            webinar.for_advanced = True
                        elif course_category == "задание 27":
                            webinar.for_expert = True
                        elif course_category == "разбор пробников":
                            webinar.for_mocks = True
                        elif course_category == "нарешка":
                            webinar.for_practice = True
                        elif course_category == "мини-щелчок":
                            webinar.for_minisnap = True
                        # Можно добавить else для обработки неизвестных категорий, если нужно
                        # else:
                        #     errors.append(f"Строка {index + 2}: Неизвестная категория курса '{row['категория курса']}'")

                    if "ссылка на обложку" in df.columns and not pd.isna(row["ссылка на обложку"]):
                        webinar.cover_url = str(row["ссылка на обложку"])

                    db.session.add(webinar)
                    db.session.flush() # Нужно для получения webinar.id перед добавлением комментария

                    # Добавляем комментарий, если он есть
                    if "комментарий" in df.columns and not pd.isna(row["комментарий"]):
                        comment = WebinarComment(
                            text=str(row["комментарий"]),
                            webinar_id=webinar.id,
                            user_id=current_user.id,
                            created_at=datetime.utcnow(),
                        )
                        db.session.add(comment)

                    imported_count += 1

                except Exception as e:
                    db.session.rollback() # Откатываем добавление этого конкретного вебинара
                    errors.append(f"Строка {index + 2}: Непредвиденная ошибка - {str(e)}")

            if errors:
                # Не откатываем всю транзакцию, чтобы успешно импортированные остались
                flash(f"Ошибки при импорте ({len(errors)}):\n" + "\n".join(errors[:10]) + ("\n..." if len(errors) > 10 else ""), "danger")
            if imported_count > 0:
                 db.session.commit()
                 flash(f"Успешно импортировано {imported_count} из {total_rows} вебинаров", "success")
            elif not errors:
                 flash("Нет данных для импорта или все вебинары уже существуют.", "info")

            # Используем .webinars_list
            return redirect(url_for("webinars.webinars_list"))

        except Exception as e:
            flash(f"Ошибка при чтении файла: {str(e)}", "danger")
            return redirect(request.url)

    # Шаблон webinars/templates/webinars/import_webinars.html
    return render_template("webinars/import_webinars.html")


@bp.route("/<int:webinar_id>/comment", methods=["POST"])
@login_required
def add_webinar_comment(webinar_id):
    webinar = Webinar.query.get_or_404(webinar_id)
    comment_text = request.form.get("comment_text")

    if comment_text:
        comment = WebinarComment(
            text=comment_text, webinar_id=webinar_id, user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash("Комментарий успешно добавлен", "success")

    # TODO: Редирект на страницу вебинара? Или оставить на списке?
    return redirect(url_for("webinars.webinars_list"))


@bp.route("/comment/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_webinar_comment(comment_id):
    comment = WebinarComment.query.get_or_404(comment_id)

    # Проверяем права на удаление (автор или админ)
    if current_user.id != comment.user_id and not current_user.is_admin:
        abort(403) # Ошибка доступа

    webinar_id = comment.webinar_id # Сохраняем для возможного редиректа
    db.session.delete(comment)
    db.session.commit()

    flash("Комментарий успешно удален", "success")
    # TODO: Редирект на страницу вебинара? Или оставить на списке?
    return redirect(url_for("webinars.webinars_list"))
