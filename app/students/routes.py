from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload  
from sqlalchemy import or_

from app import db 
from app.models import (
    Student,
    StudyPlan,
    WatchedWebinar,
    KnownTaskNumber,
    Webinar,
    TaskNumber, 
)
from app.students import bp
from .forms import StudentForm


@bp.route("/")  # Базовый URL /students
@login_required
def students_list():
    if current_user.is_educational_curator:
        abort(403)
    
    # Получаем поисковый запрос
    query = request.args.get('q', '').strip()
    
    # Получаем параметр сортировки
    sort_param = request.args.get('sort', 'date_desc')
    
    # Базовый запрос к ученикам
    students_query = Student.query

    # Если есть поисковый запрос, фильтруем
    if query:
        search_term = f"%{query}%"
        students_query = students_query.filter(
            or_(
                Student.first_name.ilike(search_term),
                Student.last_name.ilike(search_term),
                Student.platform_id.ilike(search_term)
            )
        )
    
    # Применяем сортировку в зависимости от параметра
    if sort_param == 'date_desc':
        students_query = students_query.order_by(Student.registration_date.desc().nullslast())
    elif sort_param == 'date_asc':
        students_query = students_query.order_by(Student.registration_date.asc().nullsfirst())
    elif sort_param == 'name_desc':
        students_query = students_query.order_by(Student.last_name.desc(), Student.first_name.desc())
    elif sort_param == 'target_desc':
        students_query = students_query.order_by(Student.target_score.desc().nullslast())
    elif sort_param == 'target_asc':
        students_query = students_query.order_by(Student.target_score.nullsfirst())
    elif sort_param == 'hours_desc':
        students_query = students_query.order_by(Student.hours_per_week.desc().nullslast())
    elif sort_param == 'hours_asc':
        students_query = students_query.order_by(Student.hours_per_week.nullsfirst())
    else:  # По умолчанию 'name_asc'
        students_query = students_query.order_by(Student.last_name, Student.first_name)
        
    # Получаем отсортированный список студентов
    students = students_query.all()
    
    # Для диагностики выводим в логи даты регистрации (если они есть)
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Сортировка: {sort_param}")
    for s in students[:10]:  # Первые 10 для краткости
        logger.info(f"Student: {s.first_name} {s.last_name}, Registration: {s.registration_date}")

    # Шаблон students/templates/students/students.html
    return render_template("students/students.html", students=students)


@bp.route("/<int:student_id>")
@login_required
def student_detail(student_id):
    if current_user.is_educational_curator:
        abort(403)
    student = Student.query.options(
        joinedload(Student.plans).options(  # Загружаем планы и их вебинары
            joinedload(StudyPlan.planned_webinars)
        ),
        joinedload(
            Student.watched_webinars
        ).options(  # Загружаем просмотренные вебинары и их данные
            joinedload(WatchedWebinar.webinar).options(joinedload(Webinar.task_numbers))
        ),
        joinedload(Student.known_tasks),  # Загружаем известные задания
    ).get_or_404(student_id)

    # --- Начало изменений: Расчет процента прохождения последнего плана ---
    last_plan = None
    completion_percentage = 0
    if student.plans:  # Проверяем, есть ли планы вообще
        # Находим последний по дате создания
        last_plan = (
            max(student.plans, key=lambda p: p.created_at) if student.plans else None
        )

    if (
        last_plan and last_plan.planned_webinars
    ):  # Если есть последний план и в нем есть вебинары
        total_in_plan = len(last_plan.planned_webinars)
        watched_in_plan_count = 0
        plan_webinar_ids = {pw.webinar_id for pw in last_plan.planned_webinars}
        student_watched_ids = {ww.webinar_id for ww in student.watched_webinars}

        watched_in_plan_count = len(plan_webinar_ids.intersection(student_watched_ids))

        if total_in_plan > 0:
            completion_percentage = round((watched_in_plan_count / total_in_plan) * 100)
    # --- Конец изменений ---

    watched_webinar_ids = {w.webinar_id for w in student.watched_webinars}
    known_task_numbers = {task.task_number for task in student.known_tasks}

    # Получаем список всех номеров заданий для формы
    all_tasks = TaskNumber.query.order_by(TaskNumber.number).all()
    # Получаем все вебинары для формы добавления просмотренных
    all_webinars = (
        Webinar.query.options(joinedload(Webinar.task_numbers))
        .order_by(Webinar.date.desc(), Webinar.id.desc())
        .all()
    )

    # Получаем статистику вебинаров по номерам заданий
    task_stats = {}
    
    # Получаем все вебинары с заданиями
    webinars_with_tasks = (
        Webinar.query
        .options(joinedload(Webinar.task_numbers))
        .all()
    )
    
    # Собираем статистику по каждому номеру задания
    for webinar in webinars_with_tasks:
        for task in webinar.task_numbers:
            task_num = task.number
            if task_num not in task_stats:
                task_stats[task_num] = {
                    'total': 0,
                    'watched': 0
                }
            task_stats[task_num]['total'] += 1
            if webinar.id in watched_webinar_ids:
                task_stats[task_num]['watched'] += 1

    # Расчет необходимых заданий для отображения (как в view_study_plan)
    target_score = student.target_score or 80
    required_tasks = set()
    if target_score <= 70:
        required_tasks = {
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            9,
            10,
            11,
            12,
            14,
            16,
            18,
            19,
            20,
            21,
            22,
        }
    elif target_score <= 80:
        required_tasks = {
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            14,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
        }
    elif target_score <= 85:
        required_tasks = {
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            25,
        }
    elif target_score <= 90:
        required_tasks = set(range(1, 26))
    elif target_score <= 95:
        required_tasks = {
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            27,
        }
    else:
        required_tasks = set(range(1, 28))

    # Шаблон students/templates/students/student_detail.html
    return render_template(
        "students/student_detail.html",
        student=student,
        watched_webinar_ids=watched_webinar_ids,
        watched_webinars=sorted(
            student.watched_webinars, key=lambda x: x.watched_at, reverse=True
        ),
        known_task_numbers=known_task_numbers,
        all_tasks=all_tasks,
        all_webinars=all_webinars,
        required_tasks=required_tasks,
        study_plans=sorted(student.plans, key=lambda x: x.created_at, reverse=True),
        # --- Начало изменений: Передача данных о плане ---
        last_plan=last_plan,
        completion_percentage=completion_percentage,
        # --- Конец изменений ---
        task_stats=task_stats,
    )


@bp.route("/new", methods=["GET", "POST"])
@login_required
def student_new():
    if current_user.is_educational_curator:
        abort(403)
    form = StudentForm()
    if form.validate_on_submit():
        # Проверяем уникальность Platform ID
        existing_student_platform = Student.query.filter_by(
            platform_id=form.platform_id.data
        ).first()
        if existing_student_platform:
            flash("Студент с таким Platform ID уже существует.", "danger")
            return render_template(
                "students/student_form.html", title="Добавление ученика", form=form
            )

        student = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            platform_id=form.platform_id.data,
            target_score=form.target_score.data,
            hours_per_week=form.hours_per_week.data,
            needs_python_basics=form.needs_python_basics.data,
            initial_score=form.initial_score.data,  # Будет None, если не введено
            notes=form.notes.data,
            # created_by_id=current_user.id # Добавим позже, если нужно
        )
        db.session.add(student)
        db.session.commit()
        flash("Ученик успешно добавлен!", "success")
        return redirect(url_for("students.student_detail", student_id=student.id))

    # Шаблон students/templates/students/student_form.html
    return render_template(
        "students/student_form.html", title="Добавление ученика", form=form
    )


@bp.route("/<int:student_id>/delete", methods=["POST"])
@login_required
def student_delete(student_id):
    if current_user.is_educational_curator:
        abort(403)
    
    student = Student.query.get_or_404(student_id)
    
    try:
        # Удаляем студента
        db.session.delete(student)
        db.session.commit()
        flash(f"Ученик {student.first_name} {student.last_name} успешно удален.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении ученика: {str(e)}", "danger")
    
    return redirect(url_for("students.students_list"))


@bp.route("/<int:student_id>/confirm_delete", methods=["GET"])
@login_required
def confirm_student_delete(student_id):
    if current_user.is_educational_curator:
        abort(403)
    
    student = Student.query.get_or_404(student_id)
    return render_template("students/confirm_delete.html", student=student)


@bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def student_edit(student_id):
    if current_user.is_educational_curator:
        abort(403)
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)  # Предзаполняем форму данными студента

    if form.validate_on_submit():
        # Проверяем уникальность Platform ID (если он изменился)
        if student.platform_id != form.platform_id.data:
            existing_student_platform = Student.query.filter(
                Student.platform_id == form.platform_id.data, Student.id != student.id
            ).first()
            if existing_student_platform:
                flash("Студент с таким Platform ID уже существует.", "danger")
                return render_template(
                    "students/student_form.html",
                    title="Редактирование ученика",
                    form=form,
                    student=student,
                )

        # Обновляем поля студента из формы
        form.populate_obj(student)

        db.session.commit()
        flash("Данные ученика обновлены!", "success")
        return redirect(url_for("students.student_detail", student_id=student.id))

    # При GET запросе или ошибке валидации отображаем форму
    return render_template(
        "students/student_form.html",
        title="Редактирование ученика",
        form=form,
        student=student,
    )


@bp.route("/<int:student_id>/mark_webinar_watched", methods=["POST"])
@login_required
def mark_webinar_watched(student_id):
    if current_user.is_educational_curator:
        abort(403)
    """Отмечает вебинар как просмотренный (исправлено)."""
    student = Student.query.get_or_404(student_id)

    # Разрешаем всем авторизованным пользователям (кураторам) отмечать вебинары
    # Проверка на login_required уже есть в декораторе маршрута

    action = request.form.get("action")

    if action == "unwatch":
        webinar_id = request.form.get("webinar_id")
        watched = WatchedWebinar.query.filter_by(
            student_id=student_id, webinar_id=webinar_id
        ).first()
        if watched:
            db.session.delete(watched)
            db.session.commit()
            flash("Вебинар удален из просмотренных", "success")
        else:
            flash("Запись о просмотре не найдена", "warning")

    elif action == "add_by_links":
        webinar_links = request.form.get("webinar_links", "").strip().split("\n")
        added_count = 0
        not_found_links = []
        already_watched_links = []
        newly_watched_webinars = (
            []
        )  # Сохраняем добавленные вебинары для проверки заданий

        for link in webinar_links:
            link = link.strip()
            if not link:
                continue
            webinar = Webinar.query.filter_by(url=link).first()
            if webinar:
                existing = WatchedWebinar.query.filter_by(
                    student_id=student_id, webinar_id=webinar.id
                ).first()
                if not existing:
                    watched = WatchedWebinar(
                        student_id=student_id,
                        webinar_id=webinar.id,
                        created_by_id=current_user.id,
                    )
                    db.session.add(watched)
                    added_count += 1
                    newly_watched_webinars.append(webinar)  # Добавляем вебинар
                else:
                    already_watched_links.append(link)
            else:
                not_found_links.append(link)

        if added_count > 0:
            db.session.commit()
            flash(f"Успешно добавлено {added_count} вебинаров", "success")
            # Автоматически отмечаем задания как известные для добавленных вебинаров
            check_and_mark_known_tasks(student_id, newly_watched_webinars)

        if already_watched_links:
            flash(
                f"Эти вебинары уже были отмечены: {', '.join(already_watched_links)}",
                "info",
            )
        if not_found_links:
            flash(
                f"Не найдены вебинары по ссылкам: {', '.join(not_found_links)}",
                "warning",
            )

    elif action == "add_manual":
        webinar_ids = request.form.getlist("webinar_ids")
        added_count = 0
        not_found_ids = []
        already_watched_ids = []
        newly_watched_webinars = []  # Сохраняем добавленные вебинары

        for webinar_id_str in webinar_ids:
            try:
                webinar_id = int(webinar_id_str)
                webinar = Webinar.query.get(webinar_id)
                if webinar:
                    existing = WatchedWebinar.query.filter_by(
                        student_id=student_id, webinar_id=webinar_id
                    ).first()
                    if not existing:
                        watched = WatchedWebinar(
                            student_id=student_id,
                            webinar_id=webinar_id,
                            created_by_id=current_user.id,
                        )
                        db.session.add(watched)
                        added_count += 1
                        newly_watched_webinars.append(webinar)  # Добавляем вебинар
                    else:
                        already_watched_ids.append(str(webinar_id))
                else:
                    not_found_ids.append(str(webinar_id))
            except ValueError:
                flash(f"Некорректный ID вебинара: {webinar_id_str}", "warning")

        if added_count > 0:
            db.session.commit()
            flash(f"Успешно добавлено {added_count} вебинаров", "success")
            # Автоматически отмечаем задания как известные для добавленных вебинаров
            check_and_mark_known_tasks(student_id, newly_watched_webinars)

        if already_watched_ids:
            flash(
                f"Эти вебинары уже были отмечены: ID {', '.join(already_watched_ids)}",
                "info",
            )
        if not_found_ids:
            flash(f"Не найдены вебинары с ID: {', '.join(not_found_ids)}", "warning")

    else:  # Оригинальная логика одиночного добавления
        webinar_id_str = request.form.get("webinar_id")
        if not webinar_id_str:
            flash("Не указан ID вебинара", "error")
            return redirect(url_for("students.student_detail", student_id=student_id))

        try:
            webinar_id = int(webinar_id_str)
            webinar = Webinar.query.get(webinar_id)

            if not webinar:
                flash(f"Вебинар с ID {webinar_id} не найден.", "error")
                return redirect(
                    url_for("students.student_detail", student_id=student_id)
                )

            # Проверяем, не просмотрен ли уже этот вебинар
            existing = WatchedWebinar.query.filter_by(
                student_id=student_id, webinar_id=webinar_id
            ).first()

            if existing:
                flash("Этот вебинар уже отмечен как просмотренный", "warning")
            else:
                # Создаем запись WatchedWebinar
                watched_entry = WatchedWebinar(
                    student_id=student.id,  # или student=student
                    webinar_id=webinar.id,  # или webinar=webinar
                    created_by_id=current_user.id,
                )
                db.session.add(watched_entry)
                db.session.commit()
                flash("Вебинар успешно отмечен как просмотренный", "success")

                # Автоматически отмечаем задания как известные
                check_and_mark_known_tasks(
                    student_id, [webinar]
                )  # Передаем вебинар в списке

        except ValueError:
            flash(f"Некорректный ID вебинара: {webinar_id_str}", "error")
            return redirect(url_for("students.student_detail", student_id=student_id))

    return redirect(url_for("students.student_detail", student_id=student_id))


# Вспомогательная функция для проверки и отметки заданий
def check_and_mark_known_tasks(student_id, watched_webinars_list):
    student = Student.query.get(student_id)  # Получаем студента
    if not student:
        print(f"Ошибка: Студент {student_id} не найден для проверки заданий.")
        return

    tasks_to_check = set()
    for webinar in watched_webinars_list:
        # Убедимся, что задания загружены (если lazy loading)
        db.session.refresh(webinar)
        tasks_to_check.update(webinar.task_numbers)

    if not tasks_to_check:
        return  # Нет заданий для проверки

    # Загружаем все ID просмотренных вебинаров студента ОДИН РАЗ
    all_watched_ids = {
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=student_id).with_entities(
            WatchedWebinar.webinar_id
        )
    }
    # Загружаем все известные номера заданий студента ОДИН РАЗ
    existing_known_numbers = {
        kn.task_number
        for kn in KnownTaskNumber.query.filter_by(student_id=student_id).with_entities(
            KnownTaskNumber.task_number
        )
    }

    tasks_marked = 0
    tasks_marked_numbers = []

    for task in tasks_to_check:
        if task.number in existing_known_numbers:
            continue  # Задание уже известно

        # Проверяем, все ли вебинары для этого задания просмотрены
        # Загружаем ID вебинаров для задания (если не загружены)
        # db.session.refresh(task)
        task_webinar_ids = {tw.id for tw in task.webinars}

        if not task_webinar_ids:  # Если у задания нет вебинаров?
            continue

        if task_webinar_ids.issubset(
            all_watched_ids
        ):  # Все ли они есть в просмотренных?
            # Проверяем еще раз, не добавили ли мы его только что
            if task.number not in existing_known_numbers:
                known_task = KnownTaskNumber(
                    student_id=student_id, task_number=task.number
                )
                db.session.add(known_task)
                tasks_marked += 1
                tasks_marked_numbers.append(str(task.number))
                existing_known_numbers.add(
                    task.number
                )  # Добавляем в множество, чтобы не дублировать

    if tasks_marked > 0:
        db.session.commit()  # Сохраняем добавленные KnownTaskNumber
        flash(
            f"Задания №{', '.join(tasks_marked_numbers)} автоматически отмечены как изученные",
            "success",
        )


@bp.route("/<int:student_id>/tasks", methods=["POST"])
@login_required
def update_known_tasks(student_id):
    if current_user.is_educational_curator:
        abort(403)
    known_task_ids = request.form.getlist("known_tasks")

    KnownTaskNumber.query.filter_by(student_id=student_id).delete()

    for task_id in known_task_ids:
        known_task = KnownTaskNumber(student_id=student_id, task_number=int(task_id))
        db.session.add(known_task)

    db.session.commit()
    flash("Список известных заданий обновлен", "success")

    return redirect(url_for("students.student_detail", student_id=student_id))


# Новый маршрут и функция для страницы добавления вебинаров
@bp.route("/<int:student_id>/add_webinars", methods=["GET"])
@login_required
def add_webinars_page(student_id):
    if current_user.is_educational_curator:
        abort(403)
    student = Student.query.options(
        joinedload(Student.watched_webinars) # Загружаем просмотренные
    ).get_or_404(student_id)

    # Получаем все вебинары для формы ручного выбора
    all_webinars = (
        Webinar.query.options(joinedload(Webinar.task_numbers)) # Загружаем номера заданий
        .order_by(Webinar.date.desc(), Webinar.id.desc())
        .all()
    )
    
    # Получаем ID уже просмотренных вебинаров
    watched_webinar_ids = {w.webinar_id for w in student.watched_webinars}

    return render_template(
        "students/add_webinars.html", 
        student=student,
        all_webinars=all_webinars,
        watched_webinar_ids=watched_webinar_ids
    )
