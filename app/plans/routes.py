from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date

from app import db
from app.models import (
    Student,
    StudyPlan,
    PlannedWebinar,
    Webinar,
    TaskNumber,
    WatchedWebinar,
    KnownTaskNumber
)
from app.plans import bp
# Импортируем сервис для рекомендаций
from app.services.plan_service import recommend_webinars
# Используем относительный импорт для форм внутри того же пакета
# from .forms import CreatePlanForm, EditPlanForm # Формы не используются в этих роутах

# Маршрут создания плана теперь внутри 'plans' Blueprint,
# но URL остается привязанным к студенту.
# Мы можем либо оставить его здесь, либо перенести в students,
# но логически он больше относится к планам.
# Изменим URL на /new/<student_id>
@bp.route("/new/<int:student_id>", methods=["GET", "POST"])
@login_required
def create_study_plan(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        study_plan = StudyPlan(student_id=student.id, created_by_id=current_user.id)
        db.session.add(study_plan)
        db.session.flush()

        webinar_ids = request.form.getlist("webinar_ids")
        week_numbers = request.form.getlist("week_numbers")
        # Создаем словарь id: week для удобства
        weeks_map = {int(id_): int(num) for id_, num in zip(request.form.getlist("webinar_ids_hidden"), week_numbers)}

        for webinar_id in webinar_ids: # Только выбранные пользователем
            webinar_id = int(webinar_id)
            # Берем неделю из скрытого поля или ставим 1 по умолчанию
            week_number = weeks_map.get(webinar_id, 1)
            planned_webinar = PlannedWebinar(
                study_plan_id=study_plan.id,
                webinar_id=webinar_id,
                week_number=week_number,
            )
            db.session.add(planned_webinar)

        # Читаем квоты из скрытых полей формы
        quota_basic = int(request.form.get("quota_basic", 0))
        quota_advanced = int(request.form.get("quota_advanced", 0))
        advanced_task_number = request.form.get("advanced_task_number") # Может быть пустой строкой
        try:
             advanced_task_number = int(advanced_task_number) if advanced_task_number else None
        except ValueError:
             advanced_task_number = None # На случай если передано что-то не то

        # Формируем строку резюме
        summary_lines = ["План обучения создан!"]
        summary_lines.append("\n\nПодытожим ваш план на неделю:")
        if quota_basic > 0:
            plural = "а" if quota_basic % 10 == 1 and quota_basic != 11 else ("ов" if quota_basic % 10 in [0, 5, 6, 7, 8, 9] or 10 < quota_basic < 20 else "а")
            summary_lines.append(f"✔ {quota_basic} вебинар{plural} основного курса")
        if advanced_task_number and quota_advanced > 0:
            plural = "а" if quota_advanced % 10 == 1 and quota_advanced != 11 else ("ов" if quota_advanced % 10 in [0, 5, 6, 7, 8, 9] or 10 < quota_advanced < 20 else "а")
            summary_lines.append(f"✔ {quota_advanced} вебинар{plural} по заданию {advanced_task_number}")
        summary_lines.append("✔ домашняя работа к каждому вебинару")

        db.session.commit()
        # Используем сформированное сообщение
        flash("\n".join(summary_lines), "success")
        # Используем .view_study_plan
        return redirect(url_for("plans.view_study_plan", plan_id=study_plan.id))

    # Получаем необходимые данные для рекомендаций
    webinars = Webinar.query.all()
    known_tasks_rel = KnownTaskNumber.query.filter_by(student_id=student_id).all()
    known_task_numbers = {task.task_number for task in known_tasks_rel}
    watched_webinars_rel = WatchedWebinar.query.filter_by(student_id=student_id).all()
    watched_webinar_ids = {w.webinar_id for w in watched_webinars_rel}

    # Определяем, первый ли это план и процент выполнения предыдущего
    last_plan = StudyPlan.query.filter_by(student_id=student_id).order_by(StudyPlan.created_at.desc()).first()
    is_first_plan = last_plan is None
    last_plan_completion_perc = 0.0
    if last_plan:
        # Перезагружаем запланированные вебинары для последнего плана
        last_plan_planned_webinars = PlannedWebinar.query.filter_by(study_plan_id=last_plan.id).all()
        total_in_last_plan = len(last_plan_planned_webinars)
        if total_in_last_plan > 0:
            last_plan_planned_ids = {p.webinar_id for p in last_plan_planned_webinars}
            # Считаем просмотренные из ПОСЛЕДНЕГО плана
            watched_in_last_plan = WatchedWebinar.query.filter(
                WatchedWebinar.student_id == student_id,
                WatchedWebinar.webinar_id.in_(last_plan_planned_ids)
            ).count()
            last_plan_completion_perc = watched_in_last_plan / total_in_last_plan

    # Используем сервис для получения рекомендаций, передавая новые параметры
    suitable_webinars, webinar_weeks, quota_t27, quota_t26, quota_basic = recommend_webinars(
        student,
        webinars,
        known_task_numbers,
        watched_webinar_ids,
        is_first_plan=is_first_plan, # Новый параметр
        last_plan_completion_perc=last_plan_completion_perc # Новый параметр
    )
    # --- Начало изменений: Сохраняем изменения флагов студента --- 
    db.session.commit() # Сохраняем, если recommend_webinars изменил флаги deferred
    # --- Конец изменений --- 

    # Проверка на предыдущий план
    has_previous_plan = bool(last_plan and (datetime.utcnow() - last_plan.created_at).days >= 35)

    # Определяем, какое из заданий (26 или 27) используется для вывода в резюме
    advanced_task_number = 27 if quota_t27 > 0 else (26 if quota_t26 > 0 else None)
    advanced_task_quota = quota_t27 if quota_t27 > 0 else quota_t26

    # Шаблон plans/templates/plans/create_plan.html
    return render_template(
        "plans/create_plan.html",
        student=student,
        webinars=webinars, # Все вебинары для ручного добавления
        suitable_webinars=suitable_webinars, # Рекомендованные
        known_task_numbers=known_task_numbers,
        watched_webinar_ids=watched_webinar_ids,
        webinar_weeks=webinar_weeks, # Словарь {webinar_id: week_number}
        has_previous_plan=has_previous_plan,
        # Передаем рассчитанные квоты в шаблон
        quota_basic=quota_basic,
        quota_advanced=advanced_task_quota,
        advanced_task_number=advanced_task_number
    )


@bp.route("/<int:plan_id>")
@login_required
def view_study_plan(plan_id):
    plan = StudyPlan.query.options(
        db.joinedload(StudyPlan.student), # Загружаем студента сразу
        db.joinedload(StudyPlan.planned_webinars).joinedload(PlannedWebinar.webinar) # Загружаем вебинары
    ).get_or_404(plan_id)
    student = plan.student

    # Организация вебинаров по неделям
    webinars_by_week = {}
    for planned in plan.planned_webinars:
        week = planned.week_number
        if week not in webinars_by_week: webinars_by_week[week] = []
        webinars_by_week[week].append(planned)

    # Сортировка вебинаров внутри каждой недели
    for week in webinars_by_week:
        def get_category_priority(webinar): #...
            task_nums = {task.number for task in webinar.task_numbers}
            if 27 in task_nums: return 2
            if 26 in task_nums: return 1
            return 0
        def get_sortable_datetime_basic(webinar_date): #...
             dt_obj = None
             if webinar_date:
                 if isinstance(webinar_date, datetime): dt_obj = webinar_date
                 elif isinstance(webinar_date, date): dt_obj = datetime.combine(webinar_date, datetime.min.time())
             if dt_obj: return (0, dt_obj.replace(tzinfo=None))
             return (1, datetime(2000, 1, 1))
        webinars_by_week[week].sort(key=lambda p: (
             get_category_priority(p.webinar),
             get_sortable_datetime_basic(p.webinar.date)
        ))
    weeks = {week: webinars_by_week[week] for week in sorted(webinars_by_week.keys())}

    # Остальные данные для шаблона
    watched_webinar_ids = {w.webinar_id for w in WatchedWebinar.query.filter_by(student_id=plan.student.id).all()}
    known_task_numbers = {task.task_number for task in KnownTaskNumber.query.filter_by(student_id=plan.student.id).all()}
    now = datetime.utcnow()

    # Рассчитываем required_tasks для ИНФОРМАЦИОННОГО блока (с учетом initial_score)
    required_tasks = set()
    target_score = student.target_score or 80 # Дефолтный балл для расчета
    tasks_60_70 = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 22}
    tasks_70_80 = set(range(1, 13)) | {14} | set(range(16, 24))
    tasks_80_85 = set(range(1, 24)) | {25}
    tasks_85_90 = set(range(1, 26))
    tasks_90_95 = set(range(1, 26)) | {27}
    tasks_95_100 = set(range(1, 28))
    if target_score <= 70: required_tasks = tasks_60_70.copy()
    elif target_score <= 80: required_tasks = tasks_70_80.copy()
    elif target_score <= 85: required_tasks = tasks_80_85.copy()
    elif target_score <= 90: required_tasks = tasks_85_90.copy()
    elif target_score <= 95: required_tasks = tasks_90_95.copy()
    else: required_tasks = tasks_95_100.copy()
    # Откладываем 26/27 если initial_score низкий - ТОЛЬКО для отображения в блоке
    if student.initial_score is not None and student.initial_score <= 40:
        required_tasks.discard(26)
        required_tasks.discard(27)

    week_dates = {}
    if plan.created_at:
        start_date = plan.created_at
        for i in range(1, 6):
            week_start = start_date + timedelta(days=(i-1)*7)
            week_end = week_start + timedelta(days=6)
            week_dates[i] = {'start': week_start, 'end': week_end}

    # Передача данных в шаблон (без флагов is_first_plan и show_deferral_message_tX)
    return render_template(
        "plans/view_plan.html",
        plan=plan,
        weeks=weeks,
        watched_webinar_ids=watched_webinar_ids,
        now=now,
        known_task_numbers=known_task_numbers,
        timedelta=timedelta,
        required_tasks=sorted(list(required_tasks)), # Используем рассчитанные display-задания
        week_dates=week_dates,
    )


@bp.route("/<int:plan_id>/edit", methods=["GET", "POST"])
@login_required
def edit_study_plan(plan_id):
    plan = StudyPlan.query.options(
         db.joinedload(StudyPlan.student), # Оптимизация: загружаем студента
         db.joinedload(StudyPlan.planned_webinars) # и запланированные вебинары
    ).get_or_404(plan_id)
    student = plan.student # Берем студента из плана

    if request.method == "POST":
        # Очищаем старые запланированные вебинары
        PlannedWebinar.query.filter_by(study_plan_id=plan.id).delete()

        webinar_ids = request.form.getlist("webinar_ids")
        week_numbers = request.form.getlist("week_numbers")
        weeks_map = {int(id_): int(num) for id_, num in zip(request.form.getlist("webinar_ids_hidden"), week_numbers)}

        for webinar_id in webinar_ids:
            webinar_id = int(webinar_id)
            week_number = weeks_map.get(webinar_id, 1)
            planned_webinar = PlannedWebinar(
                study_plan_id=plan.id,
                webinar_id=webinar_id,
                week_number=week_number,
            )
            db.session.add(planned_webinar)

        db.session.commit()
        flash("План обучения обновлен!", "success")
        return redirect(url_for("plans.view_study_plan", plan_id=plan.id))

    # Данные для формы редактирования
    current_planned_webinars = plan.planned_webinars # Уже загружены
    current_webinar_ids = {pw.webinar_id for pw in current_planned_webinars}
    webinars = Webinar.query.all() # Все вебинары для выбора
    known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
    known_task_numbers = [task.task_number for task in known_tasks]
    watched_webinar_ids = {
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=student.id).all()
    }
    webinar_weeks = {pw.webinar_id: pw.week_number for pw in current_planned_webinars}

    # Расчет max_weekly_webinars (можно вынести в сервис?)
    total_hours_per_week = student.hours_per_week or 9
    time_for_26_27 = 0
    if student.knows_task_26 and student.knows_task_27:
        time_for_26_27 = int(total_hours_per_week * 0.5)
    elif student.knows_task_26 or student.knows_task_27:
        time_for_26_27 = int(total_hours_per_week * 0.3)
    time_for_basic = total_hours_per_week - time_for_26_27
    basic_webinars_per_week = max(1, time_for_basic // 3)
    advanced_webinars_per_week = max(0, time_for_26_27 // 4)
    max_weekly_webinars = basic_webinars_per_week + advanced_webinars_per_week

    # Шаблон plans/templates/plans/edit_plan.html
    return render_template(
        "plans/edit_plan.html",
        plan=plan,
        student=student,
        webinars=webinars,
        current_webinar_ids=current_webinar_ids,
        known_task_numbers=known_task_numbers,
        watched_webinar_ids=watched_webinar_ids,
        webinar_weeks=webinar_weeks,
        max_weekly_webinars=max_weekly_webinars,
    )


@bp.route("/<int:plan_id>/delete", methods=["POST"])
@login_required
def delete_study_plan(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    student_id = plan.student_id # Сохраняем для редиректа

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
    plan = StudyPlan.query.get_or_404(plan_id)

    if not current_user.is_admin and current_user.id != plan.created_by_id:
        flash("У вас нет прав для выполнения этого действия", "danger")
        return redirect(url_for("plans.view_study_plan", plan_id=plan_id))

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
    webinars_in_plan = Webinar.query.filter(Webinar.id.in_(webinar_ids)).options(db.selectinload(Webinar.task_numbers)).all()
    for webinar in webinars_in_plan:
         for task in webinar.task_numbers:
             tasks_to_check.add(task)

    tasks_marked = 0
    existing_known_numbers = {
        kn.task_number for kn in KnownTaskNumber.query.filter_by(student_id=plan.student_id)
    }

    for task in tasks_to_check:
        if task.number in existing_known_numbers:
            continue # Задание уже известно

        # Проверяем, все ли вебинары для этого задания просмотрены
        task_webinar_ids = {tw.id for tw in task.webinars} # ID всех вебов для этого задания
        if task_webinar_ids.issubset(existing_watched_ids): # Все ли они есть в просмотренных?
            known_task = KnownTaskNumber(
                student_id=plan.student_id, task_number=task.number
            )
            db.session.add(known_task)
            tasks_marked += 1
            existing_known_numbers.add(task.number) # Добавляем в известные, чтобы не проверять снова

    if tasks_marked > 0:
        db.session.commit()
        flash(f"{tasks_marked} заданий автоматически отмечены как изученные", "success")

    return redirect(url_for("plans.view_study_plan", plan_id=plan_id))
