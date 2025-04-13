import os
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import or_, and_, case, func
from sqlalchemy.engine.row import Row
import re
from flask_wtf.csrf import generate_csrf
import pymorphy3

from app import db
from app.models import (
    Webinar,
    TaskNumber,
    WebinarComment,
    User,
    WatchedWebinar,
    WebinarTask,
)
from app.webinars import bp
from app.webinars.forms import WebinarForm, WebinarTaskForm

# Инициализация pymorphy2 (лучше делать один раз)
morph = pymorphy3.MorphAnalyzer()


@bp.route("/")  # Базовый URL /webinars
@login_required
def webinars_list():
    query = request.args.get("q", "").strip()
    webinars = _get_filtered_webinars_query(query)

    watched_webinar_ids = {w.webinar_id for w in WatchedWebinar.query.all()}
    task_form = WebinarTaskForm()

    return render_template(
        "webinars/webinars.html",
        webinars=webinars,
        watched_webinar_ids=watched_webinar_ids,
        task_form=task_form,
        search_query=query,  # Передаем запрос в шаблон
    )


# Новый маршрут для AJAX-запросов фильтрации
@bp.route("/filter")
@login_required
def filter_webinars():
    query = request.args.get("q", "").strip()
    webinars = _get_filtered_webinars_query(query)

    watched_webinar_ids = {w.webinar_id for w in WatchedWebinar.query.all()}
    task_form = WebinarTaskForm()  # Добавляем создание формы задач

    # Возвращаем отрендеренный ОСНОВНОЙ шаблон с отфильтрованными данными
    return render_template(
        "webinars/webinars.html",
        webinars=webinars,
        watched_webinar_ids=watched_webinar_ids,
        task_form=task_form,  # Передаем форму задач
        search_query=query,  # Передаем запрос
        current_user=current_user,  # current_user нужен для кнопок удаления/редактирования
    )


# Вспомогательная функция для получения отфильтрованного и ОТСОРТИРОВАННОГО СПИСКА вебинаров
def _get_filtered_webinars_query(query):
    # Базовый запрос с загрузкой связанных данных
    base_query = Webinar.query.options(
        joinedload(Webinar.created_by),
        selectinload(Webinar.comments).joinedload(WebinarComment.user),
        selectinload(Webinar.task_numbers),
        selectinload(Webinar.tasks).joinedload(WebinarTask.created_by),
    )

    if query:
        # --- Упрощенный поиск по подстроке ---
        final_filter = None
        term_ilike = f"%{query}%" # Ищем вхождение строки запроса
        task_number_filter = None

        # Проверка на номер задания
        match_num = re.fullmatch(r"(\d+)", query)
        match_num_hash = re.fullmatch(r"№(\d+)", query)
        if match_num:
            task_number_filter = Webinar.task_numbers.any(
                TaskNumber.number == int(match_num.group(1))
            )
        elif match_num_hash:
            task_number_filter = Webinar.task_numbers.any(
                TaskNumber.number == int(match_num_hash.group(1))
            )

        # Формируем условия поиска по основным полям + задачам + комментариям
        conditions = [
            Webinar.title.ilike(term_ilike),
            Webinar.url.ilike(term_ilike),
            Webinar.tasks.any(WebinarTask.text.ilike(term_ilike)),
            Webinar.comments.any(WebinarComment.text.ilike(term_ilike)),
        ]
        if task_number_filter is not None:
            conditions.append(task_number_filter)

        final_filter = or_(*conditions)
        # --- Конец упрощенного поиска по подстроке ---

        # --- Применение фильтра и получение результатов ---
        if final_filter is not None:
            filtered_webinars = base_query.filter(final_filter).all()
        else:
            filtered_webinars = [] # На случай, если final_filter не создался

        # --- Ранжирование и сортировка в Python (используем только исходный query) ---
        if not filtered_webinars:
             return [] # Если SQL фильтр ничего не нашел

        search_term_for_ranking = query.lower() # Для регистронезависимого сравнения в Python
        term_pattern = re.compile(re.escape(search_term_for_ranking), re.IGNORECASE)

        webinars_with_scores = []
        title_weight = 5
        task_num_weight = 4
        comment_weight = 2
        task_text_weight = 3 # Оставляем вес для задач
        url_weight = 1
        # exact_word_bonus больше не нужен в этой логике

        for webinar in filtered_webinars:
            score = 0
            term_score = 0 # Считаем очки для единственного термина - query

            found_in_title = term_pattern.search(webinar.title)
            found_in_tasks = any(term_pattern.search(task.text) for task in webinar.tasks)
            found_in_comments = any(term_pattern.search(comment.text) for comment in webinar.comments)
            # Упрощенный поиск в URL - только если query содержит цифры (похоже на ID)
            found_in_url = bool(re.search(r'\d', query) and term_pattern.search(webinar.url))

            task_nums = {t.number for t in webinar.task_numbers}
            is_task_num_match = False
            if match_num:
                is_task_num_match = int(match_num.group(1)) in task_nums
            elif match_num_hash:
                 is_task_num_match = int(match_num_hash.group(1)) in task_nums

            if found_in_title: term_score += title_weight
            if found_in_tasks: term_score += task_text_weight
            if found_in_comments: term_score += comment_weight
            if found_in_url: term_score += url_weight
            if is_task_num_match: term_score += task_num_weight

            score = term_score # Финальный счет равен счету для query
            webinars_with_scores.append((webinar, score))

        # Сортировка
        webinars_with_scores.sort(
            key=lambda item: (item[1], item[0].date is None, item[0].date, item[0].id),
            reverse=True,
        )

        return [item[0] for item in webinars_with_scores]

    else:
        # --- Если нет запроса query - простой запрос всех вебинаров с сортировкой по дате ---
        return base_query.order_by(
            Webinar.date.desc().nullslast(), Webinar.id.desc()
        ).all()


@bp.route("/import", methods=["GET", "POST"])
@login_required  # Возможно, стоит ограничить права до admin_required?
def import_webinars():
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен
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
                flash(
                    f'Отсутствуют обязательные колонки: {", ".join(missing_columns)}',
                    "danger",
                )
                return redirect(request.url)

            total_rows = len(df)
            imported_count = 0
            errors = []

            for index, row in df.iterrows():
                try:
                    if pd.isna(row["название вебинара"]) or pd.isna(
                        row["ссылка на вебинар"]
                    ):
                        errors.append(
                            f"Строка {index + 2}: Отсутствуют обязательные поля"
                        )
                        continue

                    # Проверка на дубликат по URL
                    existing_webinar = Webinar.query.filter_by(
                        url=str(row["ссылка на вебинар"])
                    ).first()
                    if existing_webinar:
                        # Опционально: можно обновлять существующий вебинар или пропускать
                        errors.append(
                            f"Строка {index + 2}: Вебинар с таким URL уже существует (ID: {existing_webinar.id})"
                        )
                        continue

                    webinar = Webinar(
                        title=str(row["название вебинара"]),
                        url=str(row["ссылка на вебинар"]),
                        created_by_id=current_user.id,
                    )

                    if "дата вебинара" in df.columns and not pd.isna(
                        row["дата вебинара"]
                    ):
                        try:
                            webinar.date = pd.to_datetime(row["дата вебинара"]).date()
                        except Exception as e:
                            errors.append(
                                f"Строка {index + 2}: Неверный формат даты ({e})"
                            )

                    if "номера заданий" in df.columns and not pd.isna(
                        row["номера заданий"]
                    ):
                        task_numbers_str = str(row["номера заданий"])
                        try:
                            task_numbers_list = [
                                int(num.strip())
                                for num in task_numbers_str.split(",")
                                if num.strip().isdigit()
                            ]
                            for num in task_numbers_list:
                                task = TaskNumber.query.filter_by(number=num).first()
                                if not task:
                                    # Если задание не найдено, можно его создать или выдать ошибку
                                    # task = TaskNumber(number=num)
                                    # db.session.add(task)
                                    errors.append(
                                        f"Строка {index + 2}: Задание с номером {num} не найдено в базе."
                                    )
                                    continue  # Пропускаем добавление этого номера
                                if task not in webinar.task_numbers:
                                    webinar.task_numbers.append(task)
                        except Exception as e:
                            errors.append(
                                f"Строка {index + 2}: Ошибка обработки номеров заданий ({e})"
                            )

                    if "тип решения" in df.columns and not pd.isna(row["тип решения"]):
                        solution_type = str(row["тип решения"]).lower()
                        webinar.is_programming = any(
                            term in solution_type
                            for term in ["прогой", "программирование", "программный"]
                        )
                        webinar.is_manual = any(
                            term in solution_type
                            for term in ["руками", "ручное", "ручной"]
                        )
                        webinar.is_excel = any(
                            term in solution_type
                            for term in ["excel", "эксель", "таблиц"]
                        )

                    if "номер дз" in df.columns and not pd.isna(row["номер дз"]):
                        try:
                            webinar.homework_number = int(row["номер дз"])
                        except ValueError:
                            errors.append(
                                f"Строка {index + 2}: Неверный формат номера ДЗ"
                            )

                    if "категория" in df.columns and not pd.isna(row["категория"]):
                        try:
                            category_val = int(row["категория"])
                            if category_val in [1, 2, 3]:
                                webinar.category = category_val
                            else:
                                errors.append(
                                    f"Строка {index + 2}: Неверное значение категории ({category_val})"
                                )
                        except ValueError:
                            errors.append(
                                f"Строка {index + 2}: Неверный формат категории"
                            )

                    if "категория курса" in df.columns and not pd.isna(
                        row["категория курса"]
                    ):
                        course_category = (
                            str(row["категория курса"]).lower().strip()
                        )  # Добавим strip() на всякий случай

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

                    if "ссылка на обложку" in df.columns and not pd.isna(
                        row["ссылка на обложку"]
                    ):
                        webinar.cover_url = str(row["ссылка на обложку"])

                    db.session.add(webinar)
                    db.session.flush()  # Нужно для получения webinar.id перед добавлением комментария

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
                    db.session.rollback()  # Откатываем добавление этого конкретного вебинара
                    errors.append(
                        f"Строка {index + 2}: Непредвиденная ошибка - {str(e)}"
                    )

            if errors:
                # Не откатываем всю транзакцию, чтобы успешно импортированные остались
                flash(
                    f"Ошибки при импорте ({len(errors)}):\n"
                    + "\n".join(errors[:10])
                    + ("\n..." if len(errors) > 10 else ""),
                    "danger",
                )
            if imported_count > 0:
                db.session.commit()
                flash(
                    f"Успешно импортировано {imported_count} из {total_rows} вебинаров",
                    "success",
                )
            elif not errors:
                flash("Нет данных для импорта или все вебинары уже существуют.", "info")

            # Используем .webinars_list
            return redirect(url_for("webinars.webinars_list"))

        except Exception as e:
            flash(f"Ошибка при чтении файла: {str(e)}", "danger")
            return redirect(request.url)

    # Шаблон webinars/templates/webinars/import_webinars.html
    return render_template("webinars/import_webinars.html")


@bp.route("/<int:webinar_id>/edit", methods=["GET", "POST"])
@login_required
def edit_webinar(webinar_id):
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен

    webinar = Webinar.query.options(selectinload(Webinar.task_numbers)).get_or_404(
        webinar_id
    )

    form = WebinarForm(obj=webinar)

    # Преобразуем список номеров заданий в строку для формы
    if webinar.task_numbers:
        form.task_numbers.data = ", ".join(
            sorted([str(task.number) for task in webinar.task_numbers])
        )

    # Устанавливаем значение для course_category
    # Найдем ключ в COURSE_CATEGORY_CHOICES, соответствующий булевым флагам вебинара
    selected_course_category = ""
    if webinar.for_beginners:
        selected_course_category = "python с нуля"
    elif webinar.for_basic:
        selected_course_category = "основной курс"
    elif webinar.for_advanced:
        selected_course_category = "хард прога"
    elif webinar.for_expert:
        selected_course_category = "задание 27"
    elif webinar.for_mocks:
        selected_course_category = "разбор пробников"
    elif webinar.for_practice:
        selected_course_category = "нарешка"
    elif webinar.for_minisnap:
        selected_course_category = "мини-щелчок"
    form.course_category.data = selected_course_category

    if form.validate_on_submit():
        # Обновляем основные поля
        webinar.title = form.title.data
        webinar.url = form.url.data
        webinar.date = form.date.data
        webinar.cover_url = form.cover_url.data

        # Обновляем тип решения
        webinar.is_programming = form.is_programming.data
        webinar.is_manual = form.is_manual.data
        webinar.is_excel = form.is_excel.data

        # Обновляем категорию
        webinar.category = int(form.category.data) if form.category.data else None

        # Обновляем категорию курса на основе выбора в SelectField
        selected_course = form.course_category.data
        webinar.for_beginners = selected_course == "python с нуля"
        webinar.for_basic = selected_course == "основной курс"
        webinar.for_advanced = selected_course == "хард прога"
        webinar.for_expert = selected_course == "задание 27"
        webinar.for_mocks = selected_course == "разбор пробников"
        webinar.for_practice = selected_course == "нарешка"
        webinar.for_minisnap = selected_course == "мини-щелчок"

        # Обновляем номера заданий
        current_tasks = {task.number for task in webinar.task_numbers}
        new_task_numbers_str = form.task_numbers.data
        new_tasks = set()
        if new_task_numbers_str:
            try:
                new_tasks = {
                    int(num.strip())
                    for num in new_task_numbers_str.split(",")
                    if num.strip().isdigit()
                }
            except ValueError:
                flash("Ошибка в формате номеров заданий", "danger")
                # Можно не продолжать сохранение или обработать иначе
                return render_template(
                    "webinars/edit_webinar.html", form=form, webinar=webinar
                )

        # Задачи для добавления
        tasks_to_add = new_tasks - current_tasks
        for num in tasks_to_add:
            task = TaskNumber.query.filter_by(number=num).first()
            if task:
                webinar.task_numbers.append(task)
            else:
                flash(
                    f"Задание с номером {num} не найдено в базе и не было добавлено.",
                    "warning",
                )

        # Задачи для удаления
        tasks_to_remove = current_tasks - new_tasks
        tasks_objects_to_remove = [
            task for task in webinar.task_numbers if task.number in tasks_to_remove
        ]
        for task in tasks_objects_to_remove:
            webinar.task_numbers.remove(task)

        try:
            db.session.commit()
            flash("Вебинар успешно обновлен!", "success")
            return redirect(url_for("webinars.webinars_list"))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при сохранении вебинара: {str(e)}", "danger")

    elif request.method == "POST":
        # Если форма не прошла валидацию при POST-запросе
        flash("Пожалуйста, исправьте ошибки в форме.", "danger")

    # Для GET-запроса или если валидация не прошла
    return render_template("webinars/edit_webinar.html", form=form, webinar=webinar)


@bp.route("/<int:webinar_id>/delete", methods=["POST"])
@login_required
def delete_webinar(webinar_id):
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен

    webinar = Webinar.query.get_or_404(webinar_id)

    try:
        # Удаляем связанные комментарии (если настроено каскадное удаление, это не обязательно)
        # WebinarComment.query.filter_by(webinar_id=webinar.id).delete()
        
        # Удаляем сам вебинар
        db.session.delete(webinar)
        db.session.commit()
        flash(f'Вебинар "{webinar.title}" успешно удален.', "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении вебинара: {str(e)}", "danger")

    return redirect(url_for("webinars.webinars_list"))


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
        abort(403)  # Ошибка доступа

    webinar_id = comment.webinar_id  # Сохраняем для возможного редиректа
    db.session.delete(comment)
    db.session.commit()

    flash("Комментарий успешно удален", "success")
    # TODO: Редирект на страницу вебинара? Или оставить на списке?
    return redirect(url_for("webinars.webinars_list"))


@bp.route("/<int:webinar_id>/task", methods=["POST"])
@login_required
def add_webinar_task(webinar_id):
    webinar = Webinar.query.get_or_404(webinar_id)
    # Создаем экземпляр формы (данные будут взяты из request.form)
    form = WebinarTaskForm()

    if form.validate_on_submit():
        new_task = WebinarTask(
            text=form.text.data, webinar_id=webinar.id, created_by_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Задача успешно добавлена.", "success")
    else:
        # Если форма не валидна (например, пустое поле text), сообщаем об ошибке
        # Поскольку мы не рендерим шаблон с формой снова, а просто
        # перенаправляем, flash - хороший способ показать ошибку
        flash("Ошибка добавления задачи. Текст задачи не может быть пустым.", "danger")
        # Альтернативно, можно собрать ошибки из form.errors
        # flash(f'Ошибка добавления задачи: {form.errors}', 'danger')

    # Перенаправляем на страницу задач этого вебинара
    return redirect(url_for(".webinar_tasks", webinar_id=webinar_id))


@bp.route("/<int:webinar_id>/tasks")
@login_required
def webinar_tasks(webinar_id):
    webinar = Webinar.query.options(
        selectinload(Webinar.tasks).joinedload(WebinarTask.created_by)
    ).get_or_404(webinar_id)
    form = WebinarTaskForm()
    # Сортируем задачи по дате создания (сначала СТАРЫЕ)
    tasks = sorted(webinar.tasks, key=lambda t: t.created_at)
    # Генерируем CSRF токен для форм удаления
    csrf_token_value = generate_csrf()
    return render_template(
        "webinars/webinar_tasks.html", 
        webinar=webinar, 
        tasks=tasks, 
        form=form, 
        csrf_token_value=csrf_token_value,  # Передаем токен в шаблон
    )


@bp.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_webinar_task(task_id):
    task = WebinarTask.query.options(
        joinedload(WebinarTask.webinar)  # Загружаем связанный вебинар для редиректа
    ).get_or_404(task_id)
    webinar_id = task.webinar_id  # Сохраняем ID вебинара

    # Проверка прав: редактировать может автор или админ
    if current_user.id != task.created_by_id and not current_user.is_admin:
        abort(403)

    form = WebinarTaskForm(obj=task)  # Заполняем форму данными задачи

    if form.validate_on_submit():
        task.text = form.text.data
        db.session.commit()
        flash("Задача успешно обновлена.", "success")
        # Перенаправляем обратно на страницу задач вебинара
        return redirect(url_for(".webinar_tasks", webinar_id=webinar_id))
    elif request.method == "POST":
        flash("Ошибка обновления задачи. Текст не может быть пустым.", "danger")

    # Для GET запроса отображаем шаблон редактирования
    return render_template(
        "webinars/edit_webinar_task.html", form=form, task=task, webinar_id=webinar_id
    )


@bp.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_webinar_task(task_id):
    task = WebinarTask.query.get_or_404(task_id)
    webinar_id = task.webinar_id  # Сохраняем ID вебинара для редиректа

    # Проверка прав: удалить может автор или админ
    if current_user.id != task.created_by_id and not current_user.is_admin:
        abort(403)

    try:
        db.session.delete(task)
        db.session.commit()
        flash("Задача успешно удалена.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении задачи: {str(e)}", "danger")

    # Перенаправляем обратно на страницу задач вебинара
    return redirect(url_for(".webinar_tasks", webinar_id=webinar_id))
