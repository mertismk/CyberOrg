from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from flask_wtf.csrf import generate_csrf
from flask_wtf import FlaskForm
from wtforms import HiddenField

from app import db
from app.models import (
    Student,
    StudyPlan,
    PlannedWebinar,
    Webinar,
    TaskNumber,
    WatchedWebinar,
    KnownTaskNumber,
)
from app.plans import bp

# Импортируем сервис для рекомендаций
from app.services.plan_service import recommend_webinars, get_webinar_hours

# Используем относительный импорт для форм внутри того же пакета
# from .forms import CreatePlanForm, EditPlanForm # Формы не используются в этих роутах


# Форма для CSRF-защиты
class CsrfForm(FlaskForm):
    pass


# Новый маршрут для выбора заданий, которые будут включены в план
@bp.route("/select_tasks/<int:student_id>", methods=["GET"])
@login_required
def select_tasks(student_id):
    if current_user.is_educational_curator:
        abort(403)

    student = Student.query.get_or_404(student_id)
    form = CsrfForm()

    # Получаем известные задания
    known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
    known_task_numbers = {task.task_number for task in known_tasks}

    # Определяем рекомендуемые задания на основе целевого балла
    recommended_tasks = set()
    target_score = student.target_score or 80
    tasks_60_70 = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 22}
    tasks_70_80 = set(range(1, 13)) | {14} | set(range(16, 24))
    tasks_80_85 = set(range(1, 24)) | {25}
    tasks_85_90 = set(range(1, 26))
    tasks_90_95 = set(range(1, 26)) | {27}
    tasks_95_100 = set(range(1, 28))

    if target_score <= 70:
        recommended_tasks = tasks_60_70.copy()
    elif target_score <= 80:
        recommended_tasks = tasks_70_80.copy()
    elif target_score <= 85:
        recommended_tasks = tasks_80_85.copy()
    elif target_score <= 90:
        recommended_tasks = tasks_85_90.copy()
    elif target_score <= 95:
        recommended_tasks = tasks_90_95.copy()
    else:
        recommended_tasks = tasks_95_100.copy()

    # Удаляем уже изученные задания из рекомендуемых
    recommended_tasks = recommended_tasks - known_task_numbers

    return render_template(
        "plans/select_tasks.html",
        student=student,
        form=form,
        known_task_numbers=known_task_numbers,
        recommended_tasks=sorted(recommended_tasks),
    )


# Маршрут создания плана теперь внутри 'plans' Blueprint,
# но URL остается привязанным к студенту.
# Мы можем либо оставить его здесь, либо перенести в students,
# но логически он больше относится к планам.
# Изменим URL на /new/<student_id>
@bp.route("/new/<int:student_id>", methods=["GET", "POST"])
@login_required
def create_study_plan(student_id):
    if current_user.is_educational_curator:
        abort(403)
    student = Student.query.get_or_404(student_id)
    # --- Данные, нужные для GET и POST ---
    watched_webinar_ids = {
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=student_id).all()
    }
    known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
    known_task_numbers = {task.task_number for task in known_tasks}
    plan_count = StudyPlan.query.filter_by(student_id=student.id).count()
    is_first_plan = plan_count == 0
    last_plan = (
        StudyPlan.query.filter_by(student_id=student.id)
        .order_by(StudyPlan.created_at.desc())
        .first()
    )
    last_plan_completion_perc = 0
    if last_plan:
        watched_count = WatchedWebinar.query.filter(
            WatchedWebinar.student_id == student.id,
            WatchedWebinar.webinar_id.in_(
                [p.webinar_id for p in last_plan.planned_webinars]
            ),
        ).count()
        total_planned = len(last_plan.planned_webinars)
        last_plan_completion_perc = (
            int(watched_count / total_planned * 100) if total_planned > 0 else 0
        )
    # --- Конец общих данных ---

    if request.method == "POST":
        # Проверяем, является ли этот запрос отправкой формы выбора заданий
        if request.form.get("is_tasks_selection") == "1":
            # Получаем выбранные задания
            selected_tasks = set(map(int, request.form.getlist("selected_tasks")))

            if not selected_tasks:
                flash("Выберите хотя бы одно задание для плана.", "warning")
                return redirect(url_for(".select_tasks", student_id=student_id))

            # Получаем рекомендации на основе выбранных заданий
            suitable_webinars, webinar_weeks, weekly_hours_summary = (
                recommend_webinars_for_tasks(
                    student=student,
                    selected_task_numbers=selected_tasks,
                    known_task_numbers=known_task_numbers,
                    watched_webinar_ids=watched_webinar_ids,
                    is_first_plan=is_first_plan,
                )
            )

            # Разделение вебинаров на рекомендованные и остальные
            suitable_webinar_ids = {w.id for w in suitable_webinars}
            all_webinars = Webinar.query.order_by(
                Webinar.date.desc(), Webinar.id.desc()
            ).all()
            other_webinars = [
                w
                for w in all_webinars
                if w.id not in suitable_webinar_ids and w.id not in watched_webinar_ids
            ]

            # Генерируем CSRF токен для формы
            csrf_token_value = generate_csrf()

            return render_template(
                "plans/create_plan.html",
                student=student,
                webinars=all_webinars,
                suitable_webinars=suitable_webinars,
                other_webinars=other_webinars,
                known_task_numbers=known_task_numbers,
                watched_webinar_ids=watched_webinar_ids,
                webinar_weeks=webinar_weeks,
                weekly_hours_summary=weekly_hours_summary,
                required_tasks=sorted(list(selected_tasks)),
                is_first_plan=is_first_plan,
                selected_tasks=selected_tasks,
                csrf_token_value=csrf_token_value,
                get_webinar_hours=get_webinar_hours,
            )

        # Обработка финального создания плана
        # Читаем квоты из формы
        try:
            quota_t26 = int(request.form.get("quota_t26", 0))
        except ValueError:
            quota_t26 = 0
        try:
            quota_t27 = int(request.form.get("quota_t27", 0))
        except ValueError:
            quota_t27 = 0

        # --- ИЗМЕНЕНИЕ: Получаем данные из формы ---
        selected_webinar_ids = request.form.getlist(
            "webinar_ids"
        )  # ID только выбранных вебинаров
        # --- Добавляем отладочный вывод ---
        print(f"--- Saving Plan --- ")
        print(
            f"Received webinar_ids from form ({len(selected_webinar_ids)}): {selected_webinar_ids}"
        )
        if len(selected_webinar_ids) != len(set(selected_webinar_ids)):
            print("!!! WARNING: Duplicate IDs received from form!")
        # --- Конец отладочного вывода ---

        if not selected_webinar_ids:
            # flash("Не выбран ни один вебинар для плана.", "warning") # Можно раскомментировать, если нужно
            # Редирект обратно на страницу GET
            return redirect(url_for(".create_study_plan", student_id=student_id))

        study_plan = StudyPlan(student_id=student.id, created_by_id=current_user.id)
        db.session.add(study_plan)
        db.session.flush()  # Получаем ID для study_plan

        # --- ИЗМЕНЕНИЕ: Сохраняем вебинары, выбранные в форме ---
        added_count = 0
        for webinar_id_str in selected_webinar_ids:
            try:
                webinar_id = int(webinar_id_str)
                # Получаем номер недели из соответствующего поля week_numbers_webinarId
                week_number_str = request.form.get(f"week_numbers_{webinar_id}")
                try:
                    # Определяем неделю, по умолчанию 1
                    week_number = int(week_number_str) if week_number_str else 1
                    if not 1 <= week_number <= 4:
                        week_number = 1
                except (ValueError, TypeError):
                    week_number = 1  # По умолчанию неделя 1, если значение некорректно

                # Проверяем, существует ли вебинар (опционально, но безопасно)
                webinar_exists = (
                    db.session.query(Webinar.id).filter_by(id=webinar_id).scalar()
                    is not None
                )
                if webinar_exists:
                    planned_webinar = PlannedWebinar(
                        study_plan_id=study_plan.id,
                        webinar_id=webinar_id,
                        week_number=week_number,
                    )
                    db.session.add(planned_webinar)
                    added_count += 1
                else:
                    print(
                        f"Предупреждение: Вебинар с ID {webinar_id} не найден, пропущен при создании плана."
                    )
                    # Можно добавить flash-сообщение, если нужно

            except ValueError:
                print(
                    f"Предупреждение: Некорректный ID вебинара {webinar_id_str}, пропущен."
                )
                continue  # Пропускаем некорректный ID

        if added_count == 0 and selected_webinar_ids:
            # Если были выбраны ID, но ни один не прошел проверку
            db.session.rollback()  # Откатываем создание study_plan
            flash(
                "Не удалось добавить выбранные вебинары. Возможно, они были удалены.",
                "danger",
            )
            return redirect(url_for(".create_study_plan", student_id=student_id))
        elif added_count == 0:
            # Если изначально не было выбрано вебинаров (хотя проверка выше должна была сработать)
            db.session.rollback()
            flash("Не выбран ни один вебинар для плана.", "warning")
            return redirect(url_for(".create_study_plan", student_id=student_id))

        # --- Добавляем лог перед коммитом ---
        print(f"Committing {added_count} PlannedWebinar entries.")
        # --- Конец лога ---

        db.session.commit()
        flash("План обучения успешно создан!", "success")
        return redirect(url_for("plans.view_study_plan", plan_id=study_plan.id))

    # --- GET Запрос ---
    # При обычном GET запросе, перенаправляем на страницу выбора заданий
    return redirect(url_for(".select_tasks", student_id=student_id))


# Функция для получения рекомендаций на основе выбранных заданий
def recommend_webinars_for_tasks(
    student,
    selected_task_numbers,
    known_task_numbers,
    watched_webinar_ids,
    is_first_plan=True,
):
    """
    Получить рекомендации по вебинарам на основе выбранных заданий.

    Args:
        student: объект Student
        selected_task_numbers: набор номеров заданий, выбранных для плана
        known_task_numbers: набор номеров заданий, которые ученик уже знает
        watched_webinar_ids: набор ID вебинаров, которые ученик уже посмотрел
        is_first_plan: является ли это первым планом для ученика

    Returns:
        tuple: (список подходящих вебинаров, словарь номеров недель, сводка по часам в неделю)
    """
    # Получаем все вебинары с задачами
    all_webinars = Webinar.query.options(db.joinedload(Webinar.task_numbers)).all()

    # Максимальное количество часов на неделю
    max_hours_per_week = student.hours_per_week or 9  # По умолчанию 9 часов

    # Группируем вебинары по заданиям для удобства обработки
    webinars_by_task = {}
    for webinar in all_webinars:
        if webinar.id in watched_webinar_ids:
            continue  # Пропускаем уже просмотренные вебинары

        # Пропускаем ролики для начинающих по Python, если студенту не нужны основы
        if not student.needs_python_basics and webinar.title:
            # Проверяем разные варианты обозначения вебинаров для начинающих
            python_beginner_keywords = [
                "Python для начинающих",
                "основы Python",
                "базовый Python",
                "введение в Python",
                "Python с нуля",
            ]
            if any(
                keyword.lower() in webinar.title.lower()
                for keyword in python_beginner_keywords
            ):
                print(
                    f"DEBUG: Пропускаем ролик для начинающих по Python: {webinar.title} (ID: {webinar.id})"
                )
                continue

        webinar_task_numbers = {task.number for task in webinar.task_numbers}

        for task_num in webinar_task_numbers:
            if task_num not in webinars_by_task:
                webinars_by_task[task_num] = []
            webinars_by_task[task_num].append(webinar)

    # Определяем приоритет вебинаров
    def get_webinar_priority(webinar):
        if not webinar:
            return 999

        # Приоритеты категорий (ниже = важнее)
        category_priority = {
            1: 0,  # Обязательный
            2: 1,  # Повторение
            4: 2,  # Для продвинутых
            3: 3,  # Необязательный
            None: 4,  # Без категории
        }

        # Количество заданий из выбранных, которые покрывает вебинар
        webinar_task_numbers = {task.number for task in webinar.task_numbers}
        covered_tasks = webinar_task_numbers.intersection(selected_task_numbers)
        relevance_score = len(covered_tasks)

        return (
            category_priority.get(webinar.category, 4),  # Приоритет по категории
            -relevance_score,  # Больше заданий = выше приоритет
            (
                webinar.date if webinar.date else datetime(2099, 1, 1)
            ),  # Сортировка по дате
        )

    # Подготовка вебинаров для добавления
    candidate_webinars = []
    for task_num in selected_task_numbers:
        if task_num in webinars_by_task:
            for webinar in webinars_by_task[task_num]:
                if webinar not in candidate_webinars:  # Избегаем дубликатов
                    candidate_webinars.append(webinar)

    # Сортируем кандидатов по приоритету
    candidate_webinars.sort(key=get_webinar_priority)

    # Распределяем вебинары по неделям с учетом лимита часов
    suitable_webinars = []
    webinar_weeks = {}
    weekly_hours = {1: 0, 2: 0, 3: 0, 4: 0}

    for webinar in candidate_webinars:
        # Рассчитываем часы вебинара
        webinar_hours = get_webinar_hours(webinar)

        # Находим неделю с минимальной нагрузкой
        current_min_week = min(weekly_hours, key=weekly_hours.get)

        # Проверяем, не превысит ли добавление вебинара лимит часов
        if weekly_hours[current_min_week] + webinar_hours <= max_hours_per_week:
            suitable_webinars.append(webinar)
            webinar_weeks[webinar.id] = current_min_week
            weekly_hours[current_min_week] += webinar_hours

    print(
        f"DEBUG: student {student.id}, hours_per_week={max_hours_per_week}, selected_tasks={selected_task_numbers}, needs_python_basics={student.needs_python_basics}"
    )
    print(
        f"DEBUG: found {len(suitable_webinars)} suitable webinars out of {len(candidate_webinars)} candidates"
    )
    print(f"DEBUG: weekly hours: {weekly_hours}")

    return suitable_webinars, webinar_weeks, weekly_hours


@bp.route("/<int:plan_id>")
@login_required
def view_study_plan(plan_id):
    if current_user.is_educational_curator:
        abort(403)
    plan = StudyPlan.query.options(
        db.joinedload(StudyPlan.student),  # Загружаем студента сразу
        db.joinedload(StudyPlan.planned_webinars).joinedload(
            PlannedWebinar.webinar
        ),  # Загружаем вебинары
    ).get_or_404(plan_id)
    student = plan.student

    webinars_by_week = {}
    for planned in plan.planned_webinars:
        week = planned.week_number
        if week not in webinars_by_week:
            webinars_by_week[week] = []
        webinars_by_week[week].append(planned)

    # Сортировка вебинаров внутри каждой недели
    for week in webinars_by_week:
        # --- Новая функция приоритета для сортировки в плане ---
        def get_plan_view_priority(webinar):
            if not webinar:
                return 4  # На случай отсутствия вебинара
            if webinar.category == 1:  # Обязательный
                return 0
            elif webinar.category == 2:  # Повторение
                return 1
            elif webinar.for_advanced:  # Для продвинутых (Предполагаем флаг)
                return 2
            elif webinar.category == 3:  # Необязательный
                return 3
            else:  # Все остальные
                return 3  # Приоритет как у необязательных

        def get_sortable_datetime_basic(webinar_date):  # ... Остается без изменений
            dt_obj = None
            if webinar_date:
                if isinstance(webinar_date, datetime):
                    dt_obj = webinar_date
                elif isinstance(webinar_date, date):
                    dt_obj = datetime.combine(webinar_date, datetime.min.time())
            if dt_obj:
                return (0, dt_obj.replace(tzinfo=None))
            return (1, datetime(2000, 1, 1))

        webinars_by_week[week].sort(
            key=lambda p: (
                get_plan_view_priority(
                    p.webinar
                ),  # Используем новую функцию приоритета
                get_sortable_datetime_basic(p.webinar.date),
            )
        )
    weeks = {week: webinars_by_week[week] for week in sorted(webinars_by_week.keys())}

    # Остальные данные для шаблона
    watched_webinar_ids = {
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=plan.student.id).all()
    }

    known_task_numbers = {
        task.task_number
        for task in KnownTaskNumber.query.filter_by(student_id=plan.student.id).all()
    }
    now = datetime.utcnow()

    # Рассчитываем required_tasks для ИНФОРМАЦИОННОГО блока (с учетом initial_score)
    required_tasks = set()
    target_score = student.target_score or 80  # Дефолтный балл для расчета
    tasks_60_70 = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 22}
    tasks_70_80 = set(range(1, 13)) | {14} | set(range(16, 24))
    tasks_80_85 = set(range(1, 24)) | {25}
    tasks_85_90 = set(range(1, 26))
    tasks_90_95 = set(range(1, 26)) | {27}
    tasks_95_100 = set(range(1, 28))
    if target_score <= 70:
        required_tasks = tasks_60_70.copy()
    elif target_score <= 80:
        required_tasks = tasks_70_80.copy()
    elif target_score <= 85:
        required_tasks = tasks_80_85.copy()
    elif target_score <= 90:
        required_tasks = tasks_85_90.copy()
    elif target_score <= 95:
        required_tasks = tasks_90_95.copy()
    else:
        required_tasks = tasks_95_100.copy()
    # Откладываем 26/27 если initial_score низкий - ТОЛЬКО для отображения в блоке
    if student.initial_score is not None and student.initial_score <= 40:
        required_tasks.discard(26)
        required_tasks.discard(27)

    # Создаем список НЕИЗВЕСТНЫХ базовых заданий (1-25) для отображения в скобках
    basic_tasks_to_study = sorted(
        [t for t in required_tasks if t <= 25 and t not in known_task_numbers]
    )

    week_dates = {}
    if plan.created_at:
        start_date = plan.created_at
        for i in range(1, 5):
            week_start = start_date + timedelta(days=(i - 1) * 7)
            week_end = week_start + timedelta(days=6)
            week_dates[i] = {"start": week_start, "end": week_end}

    # Передача данных в шаблон
    return render_template(
        "plans/view_plan.html",
        plan=plan,
        weeks=weeks,
        watched_webinar_ids=watched_webinar_ids,
        now=now,
        known_task_numbers=known_task_numbers,
        timedelta=timedelta,
        required_tasks=sorted(list(required_tasks)),
        week_dates=week_dates,
        # Передаем список НЕИЗВЕСТНЫХ базовых заданий
        basic_tasks_to_study=basic_tasks_to_study,
    )


@bp.route("/<int:plan_id>/edit", methods=["GET", "POST"])
@login_required
def edit_study_plan(plan_id):
    if current_user.is_educational_curator:
        abort(403)
    plan = StudyPlan.query.options(
        db.joinedload(StudyPlan.student),  # Оптимизация: загружаем студента
        db.joinedload(StudyPlan.planned_webinars),  # и запланированные вебинары
    ).get_or_404(plan_id)
    student = plan.student  # Берем студента из плана

    if request.method == "POST":
        # Отладочный вывод для POST-запроса
        print("Обработка POST-запроса для редактирования плана:")
        print(f"webinar_ids: {request.form.getlist('webinar_ids')}")

        # Очищаем старые запланированные вебинары
        PlannedWebinar.query.filter_by(study_plan_id=plan.id).delete()

        webinar_ids = request.form.getlist(
            "webinar_ids"
        )  # Получаем ID только выбранных вебинаров

        for webinar_id_str in webinar_ids:  # Итерируемся только по выбранным
            try:
                webinar_id = int(webinar_id_str)
                # Получаем номер недели из соответствующего поля week_numbers_webinarId
                week_number_str = request.form.get(f"week_numbers_{webinar_id}")
                try:
                    week_number = int(week_number_str) if week_number_str else 1
                    if not 1 <= week_number <= 4:
                        week_number = 1
                except (ValueError, TypeError):
                    week_number = 1

                planned_webinar = PlannedWebinar(
                    study_plan_id=plan.id,
                    webinar_id=webinar_id,
                    week_number=week_number,
                )
                db.session.add(planned_webinar)
            except ValueError:
                # Пропускаем, если ID вебинара некорректный
                flash(
                    f"Некорректный ID вебинара в запросе: {webinar_id_str}", "warning"
                )
                continue

        db.session.commit()
        flash("План обучения обновлен!", "success")
        return redirect(url_for("plans.view_study_plan", plan_id=plan.id))

    # Данные для формы редактирования (GET)
    # Загружаем planned_webinars с вебинарами, используя явный запрос вместо свойства
    current_planned_webinars = (
        PlannedWebinar.query.options(
            db.joinedload(PlannedWebinar.webinar).joinedload(Webinar.task_numbers)
        )
        .filter_by(study_plan_id=plan.id)
        .all()
    )

    current_webinar_ids = {pw.webinar_id for pw in current_planned_webinars}
    webinars = Webinar.query.all()  # Все вебинары для выбора
    known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
    known_task_numbers = {task.task_number for task in known_tasks}
    watched_webinar_ids = {
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=student.id).all()
    }
    webinar_weeks = {pw.webinar_id: pw.week_number for pw in current_planned_webinars}

    # Выводим отладочную информацию
    print(f"Количество вебинаров в текущем плане: {len(current_planned_webinars)}")
    print(f"ID вебинаров в текущем плане: {current_webinar_ids}")
    for pw in current_planned_webinars:
        print(
            f"Вебинар ID: {pw.webinar_id}, Название: {pw.webinar.title if pw.webinar else 'Нет вебинара'}, Неделя: {pw.week_number}"
        )
    print(f"Недели вебинаров: {webinar_weeks}")

    # Проверяем наличие вебинаров в базе напрямую
    if current_webinar_ids:
        direct_webinars = Webinar.query.filter(
            Webinar.id.in_(current_webinar_ids)
        ).all()
        found_webinar_ids = {w.id for w in direct_webinars}
        missing_webinar_ids = current_webinar_ids - found_webinar_ids
        print(f"Найдено вебинаров напрямую: {len(direct_webinars)}")
        print(f"Отсутствующие вебинары: {missing_webinar_ids}")

        # Если есть отсутствующие вебинары, исправляем ситуацию - удаляем их из плана
        if missing_webinar_ids:
            print(f"Удаляю отсутствующие вебинары из плана: {missing_webinar_ids}")
            PlannedWebinar.query.filter(
                PlannedWebinar.study_plan_id == plan.id,
                PlannedWebinar.webinar_id.in_(missing_webinar_ids),
            ).delete(synchronize_session=False)
            db.session.commit()

            # Перезагружаем planned_webinars после исправления
            current_planned_webinars = (
                PlannedWebinar.query.options(
                    db.joinedload(PlannedWebinar.webinar).joinedload(
                        Webinar.task_numbers
                    )
                )
                .filter_by(study_plan_id=plan.id)
                .all()
            )
            current_webinar_ids = {pw.webinar_id for pw in current_planned_webinars}

    # Расчет max_weekly_webinars (можно вынести в сервис?)
    total_hours_per_week = student.hours_per_week or 9
    time_for_26_27 = 0

    # Проверяем, знает ли студент задания 26 и 27, просматривая известные задания
    known_task_numbers = {task.task_number for task in student.known_tasks}
    knows_task_26 = 26 in known_task_numbers
    knows_task_27 = 27 in known_task_numbers

    if knows_task_26 and knows_task_27:
        time_for_26_27 = int(total_hours_per_week * 0.5)
    elif knows_task_26 or knows_task_27:
        time_for_26_27 = int(total_hours_per_week * 0.3)
    time_for_basic = total_hours_per_week - time_for_26_27
    basic_webinars_per_week = max(1, time_for_basic // 3)
    advanced_webinars_per_week = max(0, time_for_26_27 // 4)
    max_weekly_webinars = basic_webinars_per_week + advanced_webinars_per_week

    # Прямая загрузка вебинаров плана (обходное решение)
    direct_plan_webinars = []
    if current_webinar_ids:
        print(f"Загружаю вебинары для плана. ID вебинаров: {current_webinar_ids}")
        direct_webinars = (
            Webinar.query.filter(Webinar.id.in_(current_webinar_ids))
            .options(db.joinedload(Webinar.task_numbers))
            .all()
        )

        # Выводим количество найденных вебинаров для диагностики
        print(f"Найдено {len(direct_webinars)} вебинаров из {len(current_webinar_ids)}")

        # Создаем словарь вебинар_id: вебинар для быстрого доступа
        webinar_dict = {w.id: w for w in direct_webinars}

        # Создаем структуру с неделями для каждого вебинара
        for pw in current_planned_webinars:
            if pw.webinar_id in webinar_dict:
                direct_plan_webinars.append(
                    {
                        "webinar": webinar_dict[pw.webinar_id],
                        "week_number": pw.week_number,
                    }
                )
            else:
                print(f"Вебинар с ID {pw.webinar_id} не найден в базе данных")

        print(
            f"Подготовлено {len(direct_plan_webinars)} вебинаров для отображения в плане"
        )

    # Если у нас нет direct_plan_webinars, но есть current_webinar_ids, что-то пошло не так
    if len(direct_plan_webinars) == 0 and current_webinar_ids:
        print(
            "ВНИМАНИЕ: ID вебинаров есть, но не удалось загрузить ни одного вебинара!"
        )

        # Дополнительная проверка вебинаров
        for webinar_id in current_webinar_ids:
            webinar = Webinar.query.get(webinar_id)
            if webinar:
                print(f"Вебинар ID={webinar_id} существует: {webinar.title}")
            else:
                print(f"Вебинар ID={webinar_id} не существует в базе данных!")

    # Шаблон plans/templates/plans/edit_plan.html
    return render_template(
        "plans/edit_plan.html",
        plan=plan,
        student=student,
        webinars=webinars,
        current_webinar_ids=current_webinar_ids,
        current_planned_webinars=current_planned_webinars,
        direct_plan_webinars=direct_plan_webinars,  # Добавляем прямые вебинары
        known_task_numbers=known_task_numbers,
        watched_webinar_ids=watched_webinar_ids,
        webinar_weeks=webinar_weeks,
        max_weekly_webinars=max_weekly_webinars,
    )


@bp.route("/<int:plan_id>/delete", methods=["POST"])
@login_required
def delete_study_plan(plan_id):
    if current_user.is_educational_curator:
        abort(403)
    plan = StudyPlan.query.get_or_404(plan_id)
    student_id = plan.student_id  # Сохраняем для редиректа

    if not current_user.is_admin and plan.created_by_id != current_user.id:
        flash("У вас нет прав на удаление этого плана.", "danger")
        # Редирект на страницу студента
        return redirect(url_for("students.student_detail", student_id=student_id))

    # Автоматически удаляются PlannedWebinar через cascade="all, delete-orphan"
    db.session.delete(plan)
    db.session.commit()

    flash("План обучения успешно удален!", "success")
    # Редирект на страницу студента
    return redirect(url_for("students.student_detail", student_id=student_id))


@bp.route("/<int:plan_id>/mark_all_watched", methods=["POST"])
@login_required
def mark_all_webinars_watched(plan_id):
    if current_user.is_educational_curator:
        abort(403)
    plan = StudyPlan.query.get_or_404(plan_id)

    # Разрешаем всем авторизованным пользователям (кураторам) отмечать вебинары как просмотренные
    # Ранее было ограничение: if not current_user.is_admin and current_user.id != plan.created_by_id:

    planned_webinars = PlannedWebinar.query.filter_by(study_plan_id=plan_id).all()
    webinar_ids = {pw.webinar_id for pw in planned_webinars}

    existing_watched_ids = {
        w.webinar_id for w in WatchedWebinar.query.filter_by(student_id=plan.student_id)
    }

    watched_count = 0
    newly_watched_ids = set()
    for webinar_id in webinar_ids:
        if webinar_id not in existing_watched_ids:
            watched = WatchedWebinar(
                student_id=plan.student_id,
                webinar_id=webinar_id,
                created_by_id=current_user.id,
            )
            db.session.add(watched)
            watched_count += 1
            newly_watched_ids.add(webinar_id)

    if watched_count > 0:
        db.session.commit()
        flash(f"{watched_count} вебинаров отмечены как просмотренные", "success")
        # Обновляем множество ID просмотренных
        existing_watched_ids.update(newly_watched_ids)
    else:
        flash("Все вебинары плана уже были отмечены ранее", "info")

    # --- Автоматическая отметка заданий ---
    tasks_to_check = set()
    webinars_in_plan = (
        Webinar.query.filter(Webinar.id.in_(webinar_ids))
        .options(db.selectinload(Webinar.task_numbers))
        .all()
    )
    for webinar in webinars_in_plan:
        for task in webinar.task_numbers:
            tasks_to_check.add(task)

    tasks_marked = 0
    existing_known_numbers = {
        kn.task_number
        for kn in KnownTaskNumber.query.filter_by(student_id=plan.student_id)
    }

    for task in tasks_to_check:
        if task.number in existing_known_numbers:
            continue  # Задание уже известно

        # Проверяем, все ли вебинары для этого задания просмотрены
        task_webinar_ids = {
            tw.id for tw in task.webinars
        }  # ID всех вебов для этого задания
        if task_webinar_ids.issubset(
            existing_watched_ids
        ):  # Все ли они есть в просмотренных?
            known_task = KnownTaskNumber(
                student_id=plan.student_id, task_number=task.number
            )
            db.session.add(known_task)
            tasks_marked += 1
            existing_known_numbers.add(
                task.number
            )  # Добавляем в известные, чтобы не проверять снова

    if tasks_marked > 0:
        db.session.commit()
        flash(f"{tasks_marked} заданий автоматически отмечены как изученные", "success")

    return redirect(url_for("plans.view_study_plan", plan_id=plan_id))


@bp.route("/api/recommendations/<int:student_id>")
@login_required
def get_recommendations(student_id):
    """
    API эндпоинт для получения рекомендаций по вебинарам.
    Принимает параметры quota_t26 и quota_t27 для настройки квот.
    """
    try:
        # Получаем квоты из параметров запроса
        quota_t26 = int(request.args.get("quota_t26", 0))
        quota_t27 = int(request.args.get("quota_t27", 0))

        # Получаем студента
        student = Student.query.get_or_404(student_id)

        # Получаем известные задания и просмотренные вебинары
        known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
        known_task_numbers = {task.task_number for task in known_tasks}
        watched_webinar_ids = {
            w.webinar_id
            for w in WatchedWebinar.query.filter_by(student_id=student_id).all()
        }

        # Проверяем, является ли это первым планом
        plan_count = StudyPlan.query.filter_by(student_id=student.id).count()
        is_first_plan = plan_count == 0

        # Получаем процент выполнения последнего плана
        last_plan = (
            StudyPlan.query.filter_by(student_id=student.id)
            .order_by(StudyPlan.created_at.desc())
            .first()
        )
        last_plan_completion_perc = 0
        if last_plan:
            watched_count = WatchedWebinar.query.filter(
                WatchedWebinar.student_id == student.id,
                WatchedWebinar.webinar_id.in_(
                    [p.webinar_id for p in last_plan.planned_webinars]
                ),
            ).count()
            total_planned = len(last_plan.planned_webinars)
            last_plan_completion_perc = (
                int(watched_count / total_planned * 100) if total_planned > 0 else 0
            )

        # Получаем рекомендации
        suitable_webinars, webinar_weeks, weekly_hours = recommend_webinars(
            student=student,
            known_task_numbers=known_task_numbers,
            watched_webinar_ids=watched_webinar_ids,
            is_first_plan=is_first_plan,
            last_plan_completion_perc=last_plan_completion_perc,
            quota_t26=quota_t26,
            quota_t27=quota_t27,
        )

        # Форматируем результат
        recommendations = []
        for webinar in suitable_webinars:
            week_number = webinar_weeks.get(webinar.id, 1)
            recommendations.append(
                {
                    "id": webinar.id,
                    "title": webinar.title,
                    "category": webinar.category,
                    "date": webinar.date.isoformat() if webinar.date else None,
                    "week_number": week_number,
                }
            )

        return jsonify(
            {
                "success": True,
                "recommendations": recommendations,
                "weekly_hours": weekly_hours,
            }
        )

    except ValueError as e:
        return (
            jsonify({"success": False, "error": "Неверный формат параметров квот"}),
            400,
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
