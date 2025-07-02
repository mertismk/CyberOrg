import os
from flask import render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import or_, and_, case, func
from sqlalchemy.engine.row import Row
import re
from flask_wtf.csrf import generate_csrf
import pymorphy3
from sqlalchemy.dialects import postgresql  # Для вывода SQL

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
    # Получаем год из параметров запроса или используем значение по умолчанию
    selected_year = request.args.get("year", "2026")
    try:
        selected_year = int(selected_year)
    except (ValueError, TypeError):
        selected_year = 2026  # Значение по умолчанию при ошибке

    # Получаем параметры фильтрации
    search_query = request.args.get("q", "").strip()
    course_category = request.args.get("course_category", "all")
    date_filter = request.args.get("date_filter", "all")
    solution = request.args.get("solution", "all")
    category = request.args.get("category", "all")
    task_num_str = request.args.get("task_num", "all")
    
    # Создаем и выполняем запрос с фильтрацией
    query = _get_filtered_webinars_query(
        query=search_query,
        academic_year=selected_year,
        course_category=course_category,
        date_filter=date_filter,
        solution=solution,
        category=category,
        task_num_str=task_num_str,
    )
    
    # Применяем сортировку
    if date_filter == "new":
        query = query.order_by(Webinar.date.desc().nullslast(), Webinar.id.desc())
    elif date_filter == "old":
        query = query.order_by(Webinar.date.asc().nullsfirst(), Webinar.id.asc())
    else:  # По умолчанию - старые сначала
        query = query.order_by(Webinar.date.asc().nullsfirst(), Webinar.id.asc())
    
    # Выполняем запрос
    webinars = query.all()
    
    # Получаем список доступных годов для выбора
    available_years = db.session.query(Webinar.academic_year).distinct().order_by(Webinar.academic_year).all()
    available_years = [year[0] for year in available_years]
    if not available_years or selected_year not in available_years:
        if not available_years:
            available_years = [2025, 2026]
        elif selected_year not in available_years:
            available_years.append(selected_year)
            available_years.sort()
    
    # Для удобства отладки
    current_app.logger.debug(f"DEBUG: Found {len(webinars)} webinars after filtering")

    return render_template(
        "webinars/webinars.html",
        webinars=webinars,
        available_years=available_years,
        current_year=selected_year,
        course_category=course_category,
        date_filter=date_filter,
        solution=solution,
        category=category,
        task_num=task_num_str,
        search_query=search_query,
    )


# Новый маршрут для AJAX-запросов фильтрации
@bp.route("/filter")
@login_required
def filter_webinars():
    current_app.logger.debug("--- filter_webinars route START ---")  # <--- Логгирование
    # Извлекаем все параметры из запроса
    query = request.args.get("q", "").strip()
    academic_year = request.args.get("year", "2026")
    course_category = request.args.get("course_category", "all")
    date_filter = request.args.get(
        "date_filter", "all"
    )  # По умолчанию 'all', можно изменить на 'old'
    solution = request.args.get("solution", "all")
    category = request.args.get("category", "all")
    task_num_str = request.args.get(
        "task_num", "all"
    )  # Получаем как строку (e.g., "task-5")

    try:
        academic_year = int(academic_year)
    except (ValueError, TypeError):
        academic_year = 2026  # По умолчанию, если не удалось преобразовать

    current_app.logger.debug(
        f"Received query: '{query}', year: {academic_year}, course: {course_category}, date: {date_filter}, solution: {solution}, category: {category}, task: {task_num_str}"
    )  # <--- Логгирование

    webinars_query = _get_filtered_webinars_query(
        query=query,
        academic_year=academic_year,
        course_category=course_category,
        date_filter=date_filter,
        solution=solution,
        category=category,
        task_num_str=task_num_str,
    )
    
    # Применяем сортировку
    if date_filter == "new":
        webinars_query = webinars_query.order_by(Webinar.date.desc().nullslast(), Webinar.id.desc())
    elif date_filter == "old":
        webinars_query = webinars_query.order_by(Webinar.date.asc().nullsfirst(), Webinar.id.asc())
    else:  # По умолчанию - старые сначала
        webinars_query = webinars_query.order_by(Webinar.date.asc().nullsfirst(), Webinar.id.asc())
    
    # Выполняем запрос
    webinars = webinars_query.all()
    
    current_app.logger.debug(
        f"Webinars found by _get_filtered_webinars_query: {len(webinars) if webinars else 0}"
    )  # <--- Логгирование

    watched_webinar_ids = {w.webinar_id for w in WatchedWebinar.query.all()}
    task_form = WebinarTaskForm()
    
    # Получаем список всех доступных учебных годов из базы данных
    available_years = db.session.query(Webinar.academic_year).distinct().order_by(Webinar.academic_year).all()
    available_years = [year[0] for year in available_years]
    if not available_years:
        available_years = [2025, 2026]  # Если нет данных, показываем по умолчанию

    current_app.logger.debug("--- filter_webinars route END ---")  # <--- Логгирование
    # Возвращаем отрендеренный ОСНОВНОЙ шаблон с отфильтрованными данными
    return render_template(
        "webinars/webinars.html",
        webinars=webinars,
        watched_webinar_ids=watched_webinar_ids,
        task_form=task_form,
        search_query=query,
        current_user=current_user,
        current_year=academic_year,
        available_years=available_years,
    )


# Вспомогательная функция для получения отфильтрованного и ОТСОРТИРОВАННОГО СПИСКА вебинаров
def _get_filtered_webinars_query(
    query=None,
    academic_year=2026,
    course_category="all",
    date_filter="all",
    solution="all",
    category="all",
    task_num_str="all",
):
    # Базовый запрос с загрузкой связанных данных
    webinar_query = Webinar.query.options(
        joinedload(Webinar.created_by),
        selectinload(Webinar.comments).joinedload(WebinarComment.user),
        selectinload(Webinar.task_numbers),
        selectinload(Webinar.tasks).joinedload(WebinarTask.created_by),
    )

    # Применяем фильтр по учебному году
    webinar_query = webinar_query.filter(Webinar.academic_year == academic_year)

    # Применяем фильтрацию по категории курса
    if course_category == "for_beginners":
        webinar_query = webinar_query.filter(Webinar.for_beginners == True)
    elif course_category == "for_basic":
        webinar_query = webinar_query.filter(Webinar.for_basic == True)
    elif course_category == "for_advanced":
        webinar_query = webinar_query.filter(Webinar.for_advanced == True)
    elif course_category == "for_expert":
        webinar_query = webinar_query.filter(Webinar.for_expert == True)
    elif course_category == "for_mocks":
        webinar_query = webinar_query.filter(Webinar.for_mocks == True)
    elif course_category == "for_practice":
        webinar_query = webinar_query.filter(Webinar.for_practice == True)
    elif course_category == "for_minisnap":
        webinar_query = webinar_query.filter(Webinar.for_minisnap == True)
    elif course_category == "for_summer":
        webinar_query = webinar_query.filter(Webinar.for_summer == True)

    # 1. Фильтр по текстовому запросу (q)
    if query and query.strip():
        search_text = query.strip()
        current_app.logger.debug(f"DEBUG: Applying text search filter: {search_text}")
        
        # Создаем условия для поиска по разным полям
        text_search_filter = or_(
            Webinar.title.ilike(f"%{search_text}%"),
            Webinar.url.ilike(f"%{search_text}%"),
            Webinar.tasks.any(WebinarTask.text.ilike(f"%{search_text}%")),
            Webinar.comments.any(WebinarComment.text.ilike(f"%{search_text}%")),
        )
        
        # Поиск по номеру задания (если текст поиска является числом)
        if search_text.isdigit():
            task_number_search = Webinar.task_numbers.any(TaskNumber.number == int(search_text))
            text_search_filter = or_(text_search_filter, task_number_search)

        webinar_query = webinar_query.filter(text_search_filter)

    # 2. Фильтр по типу решения (solution)
    if solution != "all":
        current_app.logger.debug(f"DEBUG: Applying solution filter: {solution}")
        if hasattr(Webinar, solution):
            webinar_query = webinar_query.filter(getattr(Webinar, solution) == True)
        else:
            current_app.logger.warning(f"DEBUG: Invalid solution value: {solution}")

    # 3. Фильтр по категории важности (category)
    if category != "all" and category.startswith("category-"):
        try:
            category_num = int(category.split("-")[-1])
            current_app.logger.debug(f"DEBUG: Applying category filter: {category_num}")
            webinar_query = webinar_query.filter(Webinar.category == category_num)
        except (ValueError, IndexError):
            current_app.logger.warning(f"DEBUG: Invalid category value: {category}")

    # 4. Фильтр по номеру задания (task_num)
    if task_num_str != "all" and task_num_str.startswith("task-"):
        try:
            task_num = int(task_num_str.split("-")[-1])
            current_app.logger.debug(f"DEBUG: Applying task number filter: {task_num}")
            webinar_query = webinar_query.filter(Webinar.task_numbers.any(TaskNumber.number == task_num))
        except (ValueError, IndexError):
            current_app.logger.warning(f"DEBUG: Invalid task_num_str value: {task_num_str}")

    # 5. Фильтр по дате (date_filter)
    if date_filter != "all":
        today = datetime.now().date()
        if date_filter == "upcoming":
            # Ближайшие вебинары (дата >= сегодня)
            current_app.logger.debug("DEBUG: Applying date filter: upcoming")
            webinar_query = webinar_query.filter(Webinar.date >= today)
        elif date_filter == "past":
            # Прошедшие вебинары (дата < сегодня)
            current_app.logger.debug("DEBUG: Applying date filter: past")
            webinar_query = webinar_query.filter(Webinar.date < today)
        elif date_filter == "new" or date_filter == "old":
            # Эти фильтры применяются только для сортировки, не для фильтрации
            current_app.logger.debug(f"DEBUG: Date filter '{date_filter}' is for sorting only")
    else:
            current_app.logger.warning(f"DEBUG: Invalid date_filter value: {date_filter}")

    return webinar_query


@bp.route("/import", methods=["GET", "POST"])
@login_required  # Возможно, стоит ограничить права до admin_required?
def import_webinars():
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен

    # При загрузке страницы отображаем форму с выбором года
    academic_year = request.args.get("year", "2026")
    try:
        academic_year = int(academic_year)
    except (ValueError, TypeError):
        academic_year = 2026
    
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
            
        # Получаем выбранный учебный год из формы
        selected_year = request.form.get("academic_year", "2026")
        try:
            selected_year = int(selected_year)
        except (ValueError, TypeError):
            selected_year = 2026

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

                    # Обработка даты
                    date_value = None
                    date_str = row.get("дата вебинара", "")
                    if isinstance(date_str, str) and date_str:
                        date_formats = ["%d.%m.%Y", "%Y-%m-%d", "%m/%d/%Y"]
                        for fmt in date_formats:
                            try:
                                date_value = datetime.strptime(date_str, fmt).date()
                                break
                            except ValueError:
                                continue
                    elif isinstance(date_str, pd.Timestamp):
                        date_value = date_str.date()

                    # Создание вебинара с учебным годом
                    webinar = Webinar(
                        title=str(row["название вебинара"]),
                        url=str(row["ссылка на вебинар"]),
                        date=date_value,
                        academic_year=selected_year,  # Устанавливаем выбранный учебный год
                        created_by_id=current_user.id,
                    )

                    # Обработка номеров заданий
                    task_nums_str = row.get("номера заданий", "")
                    if task_nums_str:
                        if isinstance(task_nums_str, (int, float)):
                            task_nums_str = str(int(task_nums_str))

                        task_nums = re.findall(r'\d+', task_nums_str)
                        for num_str in task_nums:
                            task_num = int(num_str)
                            if 1 <= task_num <= 27:
                                task_number = TaskNumber.query.filter_by(number=task_num).first()
                                if not task_number:
                                    task_number = TaskNumber(number=task_num)
                                    db.session.add(task_number)
                                    db.session.flush()  # Нужно, чтобы получить id
                                webinar.task_numbers.append(task_number)

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
            return redirect(url_for("webinars.webinars_list", year=selected_year))

        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при импорте: {str(e)}", "danger")
            current_app.logger.error(f"Import error: {str(e)}")
            return redirect(request.url)

    # При GET-запросе рендерим шаблон с формой
    # Получаем список доступных годов
    available_years = db.session.query(Webinar.academic_year).distinct().order_by(Webinar.academic_year).all()
    available_years = [year[0] for year in available_years]
    if not available_years:
        available_years = [2025, 2026]
    
    # Добавляем 2026 если его нет в списке
    if 2026 not in available_years:
        available_years.append(2026)
    
    # Сортируем годы
    available_years.sort()
    
    return render_template("webinars/import_webinars.html", available_years=available_years, current_year=academic_year)


@bp.route("/<int:webinar_id>/edit", methods=["GET", "POST"])
@login_required
def edit_webinar(webinar_id):
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен

    webinar = Webinar.query.get_or_404(webinar_id)
    form = WebinarForm(obj=webinar)

    if form.validate_on_submit():
        # Сохраняем данные из формы, но не task_numbers
        task_numbers_data = form.task_numbers.data
        category_data = form.category.data
        
        # Удаляем поля, которые требуют специальной обработки
        delattr(form, 'task_numbers')
        delattr(form, 'category')
        
        # Теперь безопасно заполняем объект
        form.populate_obj(webinar)
        
        # Обработка категории
        if category_data and category_data.strip():
            try:
                webinar.category = int(category_data)
            except (ValueError, TypeError):
                webinar.category = None
        
        # Обработка номеров заданий
        webinar.task_numbers = []  # Очищаем существующие связи
        
        if task_numbers_data and task_numbers_data.strip():
            # Добавим новые номера
            task_nums = [int(num.strip()) for num in task_numbers_data.split(',') if num.strip()]
            for num in task_nums:
                task_number = TaskNumber.query.filter_by(number=num).first()
                if not task_number:
                    task_number = TaskNumber(number=num)
                    db.session.add(task_number)
                webinar.task_numbers.append(task_number)

        try:
            db.session.commit()
            flash('Вебинар успешно обновлен!', 'success')
            return redirect(url_for('webinars.webinars_list', year=webinar.academic_year))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении вебинара: {str(e)}', 'danger')
            return redirect(url_for('webinars.edit_webinar', webinar_id=webinar.id))
    
    # Заполняем поле task_numbers для отображения в форме
    if webinar.task_numbers:
        form.task_numbers.data = ', '.join([str(task.number) for task in webinar.task_numbers])
    else:
        form.task_numbers.data = ''
    
    return render_template('webinars/edit_webinar.html', form=form, webinar=webinar)


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


@bp.route("/download_all_covers", methods=["GET", "POST"])
@login_required
def download_all_covers():
    if not current_user.is_super_admin:
        abort(403)  # Доступ запрещен

    # Получаем все вебинары с непустыми URL обложек
    webinars_with_covers = Webinar.query.filter(
        Webinar.cover_url.isnot(None), 
        Webinar.cover_url != ""
    ).all()
    
    # Подсчитываем, сколько обложек нужно скачать
    count = len(webinars_with_covers)
    
    if request.method == "POST":
        # Здесь логика скачивания обложек
        # Код для скачивания будет добавлен позже
        flash("Начато скачивание обложек. Это может занять некоторое время.", "info")
        # После скачивания перенаправляем на список вебинаров
        return redirect(url_for("webinars.webinars_list"))
    
    return render_template("webinars/download_covers.html", count=count)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create_webinar():
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен
    
    form = WebinarForm()
    
    # Устанавливаем учебный год по умолчанию (2026)
    if request.args.get("year"):
        try:
            selected_year = int(request.args.get("year"))
            form.academic_year.data = selected_year
        except (ValueError, TypeError):
            form.academic_year.data = 2026
    
    if form.validate_on_submit():
        # Сохраняем данные из формы, но не task_numbers
        task_numbers_data = form.task_numbers.data
        
        new_webinar = Webinar(
            title=form.title.data,
            url=form.url.data,
            date=form.date.data,
            academic_year=form.academic_year.data,
            is_programming=form.is_programming.data,
            is_manual=form.is_manual.data,
            is_excel=form.is_excel.data,
            for_beginners=form.for_beginners.data,
            for_basic=form.for_basic.data,
            for_advanced=form.for_advanced.data,
            for_expert=form.for_expert.data,
            for_mocks=form.for_mocks.data,
            for_practice=form.for_practice.data,
            for_minisnap=form.for_minisnap.data,
            for_summer=form.for_summer.data,
            cover_url=form.cover_url.data,
            created_by_id=current_user.id,
        )
        
        # Обработка категории
        if form.category.data and form.category.data.strip():
            try:
                new_webinar.category = int(form.category.data)
            except (ValueError, TypeError):
                new_webinar.category = None
        else:
            new_webinar.category = None
        
        # Обработка номеров заданий
        if task_numbers_data and task_numbers_data.strip():
            task_nums = [int(num.strip()) for num in task_numbers_data.split(',') if num.strip()]
            for num in task_nums:
                task_number = TaskNumber.query.filter_by(number=num).first()
                if not task_number:
                    task_number = TaskNumber(number=num)
                    db.session.add(task_number)
                new_webinar.task_numbers.append(task_number)
        
        try:
            db.session.add(new_webinar)
            db.session.commit()
            flash('Вебинар успешно создан!', 'success')
            return redirect(url_for('webinars.webinars_list', year=new_webinar.academic_year))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании вебинара: {str(e)}', 'danger')
    
    # Получаем список доступных годов для выбора
    available_years = db.session.query(Webinar.academic_year).distinct().order_by(Webinar.academic_year).all()
    available_years = [year[0] for year in available_years]
    if not available_years or 2026 not in available_years:
        if not available_years:
            available_years = [2025, 2026]
        elif 2026 not in available_years:
            available_years.append(2026)
            available_years.sort()
    
    return render_template('webinars/create_webinar.html', form=form, available_years=available_years)


@bp.route("/ajax_search")
@login_required
def ajax_search():
    current_app.logger.debug("--- ajax_search route START ---")
    # Извлекаем все параметры из запроса
    query = request.args.get("q", "").strip()
    academic_year = request.args.get("year", "2026")
    course_category = request.args.get("course_category", "all")
    date_filter = request.args.get("date_filter", "all")
    solution = request.args.get("solution", "all")
    category = request.args.get("category", "all")
    task_num_str = request.args.get("task_num", "all")

    try:
        academic_year = int(academic_year)
    except (ValueError, TypeError):
        academic_year = 2026

    current_app.logger.debug(
        f"AJAX search query: '{query}', year: {academic_year}, course: {course_category}, date: {date_filter}, solution: {solution}, category: {category}, task: {task_num_str}"
    )

    # Создаем запрос для фильтрации вебинаров
    webinars_query = _get_filtered_webinars_query(
        query=query,
        academic_year=academic_year,
        course_category=course_category,
        date_filter=date_filter,
        solution=solution,
        category=category,
        task_num_str=task_num_str,
    )
    
    # Применяем сортировку
    if date_filter == "new":
        webinars_query = webinars_query.order_by(Webinar.date.desc().nullslast(), Webinar.id.desc())
    elif date_filter == "old":
        webinars_query = webinars_query.order_by(Webinar.date.asc().nullsfirst(), Webinar.id.asc())
    else:  # По умолчанию - старые сначала
        webinars_query = webinars_query.order_by(Webinar.date.asc().nullsfirst(), Webinar.id.asc())
    
    # Выполняем запрос
    webinars = webinars_query.all()
    
    current_app.logger.debug(
        f"AJAX search found: {len(webinars) if webinars else 0} webinars"
    )

    watched_webinar_ids = {w.webinar_id for w in WatchedWebinar.query.all()}
    csrf_token_value = generate_csrf()
    
    # Рендерим только часть шаблона с вебинарами
    html = render_template(
        "webinars/_webinars_list.html",
        webinars=webinars,
        watched_webinar_ids=watched_webinar_ids,
        current_user=current_user,
        csrf_token_value=csrf_token_value,
    )
    
    return html
