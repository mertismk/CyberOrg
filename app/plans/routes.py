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
    OGETopic,
    OGETopicOrder,
    OGEParallelPlan,
    OGEParallelPlanSlot,
    OGEParallelPlanWebinar,
    OGEParallelPlanTopicOrder,
)
from app.plans import bp

# Импортируем сервис для рекомендаций
from app.services.plan_service import recommend_webinars, get_webinar_hours, get_priority_for_webinar, analyze_webinar_blocks
# Импортируем сервис для ОГЭ планов
from app.services.oge_plan_service import (
    create_oge_parallel_plan, get_oge_topics_in_order, get_plan_progress, 
    get_parallel_plan_visual_data, extend_parallel_plan, initialize_oge_topic_order,
    generate_student_message
)

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

    # Определяем рекомендуемые задания на основе целевого балла/оценки
    recommended_tasks = set()
    target_score = student.target_score or 80
    
    if student.exam_type == 'oge':
        # Для ОГЭ только задания 1-16, логика по оценкам (3-5)
        if target_score <= 3:
            recommended_tasks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
        elif target_score <= 4:
            recommended_tasks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
        else:  # target_score == 5
            recommended_tasks = set(range(1, 17))  # Все задания 1-16
    else:
        # Для ЕГЭ логика по баллам (60-100)
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


# Новый маршрут для анализа блоков вебинаров
@bp.route("/analyze_blocks/<int:student_id>", methods=["GET", "POST"])
@login_required
def analyze_blocks(student_id):
    if current_user.is_educational_curator:
        abort(403)

    student = Student.query.get_or_404(student_id)
    form = CsrfForm()

    if request.method == "POST":
        # Получаем выбранные задания из формы
        selected_tasks = set(map(int, request.form.getlist("selected_tasks")))
        include_2025_webinars = request.form.get("include_2025_webinars") == "yes"
        
        if not selected_tasks:
            flash("Выберите хотя бы одно задание для плана.", "warning")
            return redirect(url_for(".select_tasks", student_id=student_id))

        # Получаем известные задания и просмотренные вебинары
        known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
        known_task_numbers = {task.task_number for task in known_tasks}
        watched_webinar_ids = {
            w.webinar_id
            for w in WatchedWebinar.query.filter_by(student_id=student_id).all()
        }
        
        # Получаем все вебинары для анализа блоков
        webinars_query = Webinar.query.options(db.joinedload(Webinar.task_numbers))
        webinars_query = webinars_query.filter(Webinar.exam_type == student.exam_type)
        
        if not include_2025_webinars:
            webinars_query = webinars_query.filter(Webinar.academic_year == 2026)
        
        all_webinars = webinars_query.all()
        
        # Анализируем блоки вебинаров
        hours_per_week = student.hours_per_week or 9
        plan_count = StudyPlan.query.filter_by(student_id=student.id).count()
        is_first_plan = plan_count == 0
        
        # Определяем нужны ли задания 26
        needs_task_26 = 26 in selected_tasks
        
        webinar_blocks = analyze_webinar_blocks(
            all_webinars, 
            watched_webinar_ids, 
            hours_per_week, 
            student.needs_python_basics, 
            is_first_plan, 
            needs_task_26,
            include_2025_webinars
        )
        
        # Генерируем CSRF токен для формы
        csrf_token_value = generate_csrf()
        
        return render_template(
            "plans/analyze_blocks.html",
            student=student,
            webinar_blocks=webinar_blocks,
            selected_tasks=sorted(list(selected_tasks)),
            include_2025_webinars=include_2025_webinars,
            csrf_token_value=csrf_token_value,
            plan_count=plan_count,
        )

    # GET запрос - перенаправляем на выбор заданий
    return redirect(url_for(".select_tasks", student_id=student_id))


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
            
            # Получаем параметр включения вебинаров 2025 года
            include_2025_webinars = request.form.get("include_2025_webinars") == "yes"

            if not selected_tasks:
                flash("Выберите хотя бы одно задание для плана.", "warning")
                return redirect(url_for(".select_tasks", student_id=student_id))

        # Проверяем, является ли этот запрос финальным созданием плана
        elif request.form.get("final_create") == "1":
            # Обработка финального создания плана
            selected_webinar_ids = request.form.getlist("webinar_ids")
            webinar_weeks = {}
            
            # Получаем распределение по неделям из формы
            for webinar_id in selected_webinar_ids:
                week_number = request.form.get(f"week_numbers_{webinar_id}", 1)
                try:
                    webinar_weeks[webinar_id] = int(week_number)
                except ValueError:
                    webinar_weeks[webinar_id] = 1
            
            if not selected_webinar_ids:
                flash("Не выбраны вебинары для плана.", "warning")
                return redirect(url_for(".create_study_plan", student_id=student_id))
            
            # Создаем план в базе данных
            study_plan = StudyPlan(student_id=student.id, created_by_id=current_user.id)
            db.session.add(study_plan)
            db.session.flush()  # Получаем ID для study_plan

            # Сохраняем вебинары с их неделями
            added_count = 0
            for webinar_id_str in selected_webinar_ids:
                try:
                    webinar_id = int(webinar_id_str)
                    week_number = webinar_weeks.get(webinar_id_str, 1)
                    
                    # Проверяем, существует ли вебинар
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
                except ValueError:
                    continue

            if added_count == 0:
                db.session.rollback()
                flash("Не удалось добавить выбранные вебинары.", "danger")
                return redirect(url_for(".create_study_plan", student_id=student_id))

            db.session.commit()
            flash("План обучения успешно создан!", "success")
            
            # Для студентов ОГЭ перенаправляем на создание плана ОГЭ
            if student.exam_type == 'oge':
                return redirect(url_for("plans.create_oge_plan", student_id=student_id))
            else:
                return redirect(url_for("plans.view_study_plan", plan_id=study_plan.id))
        
        # Обработка формы анализа блоков - показываем страницу с ручным редактированием
        else:
            # Получаем выбранные задания из формы анализа блоков
            selected_tasks = set(map(int, request.form.getlist("selected_tasks")))
            include_2025_webinars = request.form.get("include_2025_webinars") == "yes"
            needs_python_basics = request.form.get("needs_python_basics") == "yes"
            
            if not selected_tasks:
                flash("Не выбраны задания для плана.", "warning")
                return redirect(url_for(".select_tasks", student_id=student_id))
                
            # Получаем известные задания и просмотренные вебинары
            known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
            known_task_numbers = {task.task_number for task in known_tasks}
            watched_webinar_ids = {
                w.webinar_id
                for w in WatchedWebinar.query.filter_by(student_id=student_id).all()
            }
            plan_count = StudyPlan.query.filter_by(student_id=student.id).count()
            is_first_plan = plan_count == 0
            
            # Читаем квоты блоков из формы (недельные квоты)
            block_quotas = {}
            block_keys = ['beginners', 'basic', 'advanced', 'mocks', 'practice']
            for block_key in block_keys:
                try:
                    block_quotas[block_key] = int(request.form.get(f"weekly_block_quota_{block_key}", 0))
                except ValueError:
                    block_quotas[block_key] = 0

            # Получаем рекомендации на основе выбранных заданий и квот блоков
            suitable_webinars, webinar_weeks, weekly_hours_summary, webinar_blocks = (
                recommend_webinars(
                    student=student,
                    known_task_numbers=known_task_numbers,
                    watched_webinar_ids=watched_webinar_ids,
                    is_first_plan=is_first_plan,
                    selected_task_numbers=selected_tasks,
                    include_2025_webinars=include_2025_webinars,
                    block_quotas=block_quotas,
                )
            )
            
            # Используем рекомендованные вебинары как выбранные
            selected_webinar_ids = [str(w.id) for w in suitable_webinars]
            
            if not selected_webinar_ids:
                flash("Не удалось подобрать вебинары для плана.", "warning")
                return redirect(url_for(".analyze_blocks", student_id=student_id))
            
            # Получаем все доступные вебинары для отображения в разделе "Доступные вебинары"
            all_webinars_query = Webinar.query.options(db.joinedload(Webinar.task_numbers))
            all_webinars_query = all_webinars_query.filter(Webinar.exam_type == student.exam_type)
            
            # Применяем фильтр по академическому году
            if not include_2025_webinars:
                all_webinars_query = all_webinars_query.filter(Webinar.academic_year == 2026)
                
            all_available_webinars = all_webinars_query.all()
            print(f"DEBUG: Total available webinars: {len(all_available_webinars)}")
            print(f"DEBUG: Include 2025 webinars: {include_2025_webinars}")
            
            # Отладочная информация по годам
            webinars_by_year = {}
            for webinar in all_available_webinars:
                year = webinar.academic_year
                if year not in webinars_by_year:
                    webinars_by_year[year] = 0
                webinars_by_year[year] += 1
            print(f"DEBUG: Webinars by academic year: {webinars_by_year}")

            # Вычисляем required_tasks для отображения в шаблоне
            required_tasks = set()
            target_score = student.target_score or 80
            
            if student.exam_type == 'oge':
                # Для ОГЭ только задания 1-16, логика по оценкам (3-5)
                if target_score <= 3:
                    required_tasks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
                elif target_score <= 4:
                    required_tasks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
                else:  # target_score == 5
                    required_tasks = set(range(1, 17))  # Все задания 1-16
            else:
                # Для ЕГЭ логика по баллам (60-100)
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
                
                # Откладываем 26/27 если initial_score низкий
                if student.initial_score is not None and student.initial_score <= 40:
                    required_tasks.discard(26)
                    required_tasks.discard(27)

            # Показываем страницу с ручным редактированием
            csrf_token_value = generate_csrf()
            return render_template(
                "plans/create_plan.html",
                student=student,
                selected_tasks=sorted(list(selected_tasks)),
                include_2025_webinars=include_2025_webinars,
                needs_python_basics=needs_python_basics,
                suitable_webinars=suitable_webinars,
                webinars=all_available_webinars,  # Добавляем все доступные вебинары
                webinar_weeks=webinar_weeks,
                weekly_hours_summary=weekly_hours_summary,
                webinar_blocks=webinar_blocks,
                csrf_token_value=csrf_token_value,
                get_webinar_hours=get_webinar_hours,
                required_tasks=sorted(list(required_tasks)),
                known_task_numbers=known_task_numbers,
                watched_webinar_ids=watched_webinar_ids,  # Добавляем ID просмотренных вебинаров
            )

    # --- GET Запрос ---
    # При обычном GET запросе, перенаправляем на страницу выбора заданий
    return redirect(url_for(".select_tasks", student_id=student_id))





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
    
    if student.exam_type == 'oge':
        # Для ОГЭ только задания 1-16, логика по оценкам (3-5)
        if target_score <= 3:
            required_tasks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
        elif target_score <= 4:
            required_tasks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
        else:  # target_score == 5
            required_tasks = set(range(1, 17))  # Все задания 1-16
    else:
        # Для ЕГЭ логика по баллам (60-100)
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
        # Передаем функцию расчета часов для вебинаров
        get_webinar_hours=get_webinar_hours,
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
    webinars = Webinar.query.filter(Webinar.exam_type == student.exam_type).all()  # Только вебинары нужного типа экзамена
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

    try:
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

        # Обновляем множество ID просмотренных
        existing_watched_ids.update(newly_watched_ids)

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

        # Делаем commit для всех изменений
        db.session.commit()
        
        # Для AJAX запросов не показываем flash сообщения о заданиях
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if watched_count > 0:
                flash(f"{watched_count} вебинаров отмечены как просмотренные", "success")
            else:
                flash("Все вебинары плана уже были отмечены ранее", "info")
            if tasks_marked > 0:
                flash(f"{tasks_marked} заданий автоматически отмечены как изученные", "success")

        # Для AJAX запросов возвращаем JSON, для обычных - редирект
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            message = f'Отмечено как просмотренные: {watched_count} вебинаров' if watched_count > 0 else 'Все вебинары уже отмечены как просмотренные'
            if tasks_marked > 0:
                message += f', {tasks_marked} заданий автоматически отмечены как изученные'
            return jsonify({
                'success': True,
                'message': message,
                'added_count': watched_count,
                'tasks_marked': tasks_marked
            })
        else:
            return redirect(url_for("plans.view_study_plan", plan_id=plan_id))
    
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': f'Ошибка при отметке вебинаров: {str(e)}'
            }), 500
        else:
            flash(f"Ошибка при отметке вебинаров: {str(e)}", "error")
            return redirect(url_for("plans.view_study_plan", plan_id=plan_id))


@bp.route("/api/recommendations/<int:student_id>")
@login_required
def get_recommendations(student_id):
    """
    API эндпоинт для получения рекомендаций по вебинарам.
    Квоты T26 и T27 теперь распределяются в предыдущем окне.
    """
    try:

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
        suitable_webinars, webinar_weeks, weekly_hours, webinar_blocks = recommend_webinars(
            student=student,
            known_task_numbers=known_task_numbers,
            watched_webinar_ids=watched_webinar_ids,
            is_first_plan=is_first_plan,
            include_2025_webinars=False,  # По умолчанию только 2026 год
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
                "webinar_blocks": webinar_blocks,
            }
        )

    except ValueError as e:
        return (
            jsonify({"success": False, "error": "Неверный формат параметров квот"}),
            400,
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/")
@login_required
def view_plans():
    """Отображает список всех планов обучения"""
    if current_user.is_educational_curator:
        abort(403)
        
    # Получаем все планы обучения, сортируем по дате создания (новые сверху)
    plans = StudyPlan.query.options(
        db.joinedload(StudyPlan.student),
        db.joinedload(StudyPlan.created_by)
    ).order_by(StudyPlan.created_at.desc()).all()
    
    # Группируем планы по студентам для более удобного отображения
    students_with_plans = {}
    
    for plan in plans:
        student_id = plan.student_id
        if student_id not in students_with_plans:
            students_with_plans[student_id] = {
                'student': plan.student,
                'plans': []
            }
        students_with_plans[student_id]['plans'].append(plan)
    
    return render_template(
        "plans/view_plans.html",
        students_with_plans=students_with_plans,
        title="Все планы обучения"
    )


# ========== МАРШРУТЫ ДЛЯ ОГЭ ПЛАНОВ ==========

@bp.route("/oge/create/<int:student_id>", methods=["GET", "POST"])
@login_required
def create_oge_plan(student_id):
    """Создание плана ОГЭ для студента"""
    if current_user.is_educational_curator:
        abort(403)
    
    student = Student.query.get_or_404(student_id)
    
    if student.exam_type != 'oge':
        flash("План ОГЭ может быть создан только для студентов ОГЭ", "error")
        return redirect(url_for("students.student_detail", student_id=student_id))
    
    # Проверяем, есть ли уже активный план ОГЭ
    existing_plan = OGEParallelPlan.query.filter_by(
        student_id=student_id, 
        is_active=True
    ).first()
    
    if existing_plan:
        flash("У студента уже есть активный план ОГЭ", "warning")
        return redirect(url_for(".manage_oge_plan", plan_id=existing_plan.id))
    
    if request.method == "POST":
        try:
            webinars_per_week = int(request.form.get("webinars_per_week", 1))
            hard_prog_webinars_per_week = int(request.form.get("hard_prog_webinars_per_week", 0))
            
            # Валидация
            if webinars_per_week < 1 or webinars_per_week > 3:
                flash("Количество вебинаров в неделю должно быть от 1 до 3", "error")
                return redirect(url_for(".create_oge_plan", student_id=student_id))
            
            if hard_prog_webinars_per_week < 0 or hard_prog_webinars_per_week > 1:
                flash("Количество вебинаров хард-вебинаров ОГЭ должно быть 0 или 1", "error")
                return redirect(url_for(".create_oge_plan", student_id=student_id))
            
            if webinars_per_week + hard_prog_webinars_per_week > 3:
                flash("Всего вебинаров в неделю не может быть больше 3", "error")
                return redirect(url_for(".create_oge_plan", student_id=student_id))
            
            # Создаем план
            plan = create_oge_parallel_plan(
                student=student,
                webinars_per_week=webinars_per_week,
                hard_prog_webinars_per_week=hard_prog_webinars_per_week,
                created_by_id=current_user.id
            )
            
            flash(f"План ОГЭ успешно создан для {student.full_name}", "success")
            return redirect(url_for(".manage_oge_plan", plan_id=plan.id))
            
        except Exception as e:
            flash(f"Ошибка при создании плана: {str(e)}", "error")
            return redirect(url_for(".create_oge_plan", student_id=student_id))
    
    # GET запрос - показываем форму
    return render_template(
        "plans/create_oge_plan.html",
        student=student,
        title=f"Создание плана ОГЭ - {student.full_name}"
    )


@bp.route("/oge/manage/<int:plan_id>")
@login_required
def manage_oge_plan(plan_id):
    """Управление планом ОГЭ"""
    if current_user.is_educational_curator:
        abort(403)
    
    plan = OGEParallelPlan.query.get_or_404(plan_id)
    
    # Получаем данные для визуализации
    visual_data = get_parallel_plan_visual_data(plan)
    progress = get_plan_progress(plan)
    
    return render_template(
        "plans/manage_oge_plan.html",
        plan=plan,
        visual_data=visual_data,
        progress=progress,
        generate_student_message=generate_student_message,
        title=f"План ОГЭ - {plan.student.full_name}"
    )


@bp.route("/oge/extend/<int:plan_id>", methods=["POST"])
@login_required
def extend_oge_plan(plan_id):
    """Расширение плана ОГЭ на дополнительные недели"""
    if current_user.is_educational_curator:
        abort(403)
    
    plan = OGEParallelPlan.query.get_or_404(plan_id)
    
    try:
        additional_weeks = int(request.form.get("additional_weeks", 4))
        
        if additional_weeks < 1 or additional_weeks > 12:
            flash("Количество дополнительных недель должно быть от 1 до 12", "error")
            return redirect(url_for(".manage_oge_plan", plan_id=plan_id))
        
        extend_parallel_plan(plan, additional_weeks)
        
        flash(f"План успешно расширен на {additional_weeks} недель", "success")
        
    except Exception as e:
        flash(f"Ошибка при расширении плана: {str(e)}", "error")
    
    return redirect(url_for(".manage_oge_plan", plan_id=plan_id))


@bp.route("/oge/deactivate/<int:plan_id>", methods=["POST"])
@login_required
def deactivate_oge_plan(plan_id):
    """Деактивация плана ОГЭ"""
    if current_user.is_educational_curator:
        abort(403)
    
    plan = OGEParallelPlan.query.get_or_404(plan_id)
    
    try:
        plan.is_active = False
        db.session.commit()
        
        flash("План ОГЭ деактивирован", "success")
        
    except Exception as e:
        flash(f"Ошибка при деактивации плана: {str(e)}", "error")
    
    return redirect(url_for("students.student_detail", student_id=plan.student_id))


@bp.route("/oge/init-topics", methods=["POST"])
@login_required
def init_oge_topics():
    """Инициализация тем ОГЭ (только для администраторов)"""
    if not current_user.is_admin:
        abort(403)
    
    try:
        initialize_oge_topic_order()
        flash("Темы ОГЭ успешно инициализированы", "success")
    except Exception as e:
        flash(f"Ошибка при инициализации тем: {str(e)}", "error")
    
    return redirect(url_for("main.index"))


@bp.route("/oge/topics")
@login_required
def manage_oge_topics():
    """Управление темами ОГЭ и их приоритетами"""
    if not current_user.is_admin:
        abort(403)
    
    # Получаем все темы ОГЭ с их приоритетами
    topics = OGETopic.query.filter_by(is_active=True).order_by(
        OGETopic.priority.asc().nullslast(),
        OGETopic.name.asc()
    ).all()
    
    return render_template(
        "plans/manage_oge_topics.html",
        topics=topics,
        title="Управление темами ОГЭ"
    )


@bp.route("/oge/topics/update-priority", methods=["POST"])
@login_required
def update_oge_topic_priority():
    """Обновление приоритета темы ОГЭ"""
    if not current_user.is_admin:
        abort(403)
    
    try:
        topic_id = int(request.form.get("topic_id"))
        priority = request.form.get("priority")
        
        topic = OGETopic.query.get_or_404(topic_id)
        
        if priority == "" or priority is None:
            topic.priority = None
        else:
            priority_int = int(priority)
            if priority_int < 1 or priority_int > 4:
                flash("Приоритет должен быть от 1 до 4", "error")
                return redirect(url_for(".manage_oge_topics"))
            topic.priority = priority_int
        
        db.session.commit()
        flash(f"Приоритет темы '{topic.name}' обновлен", "success")
        
    except ValueError:
        flash("Неверный формат приоритета", "error")
    except Exception as e:
        flash(f"Ошибка при обновлении приоритета: {str(e)}", "error")
    
    return redirect(url_for(".manage_oge_topics"))


@bp.route("/oge/mark-webinar-watched/<int:plan_id>/<int:webinar_id>", methods=["POST"])
@login_required
def mark_oge_webinar_watched(plan_id, webinar_id):
    """Отметить вебинар как просмотренный в плане ОГЭ"""
    if current_user.is_educational_curator:
        abort(403)
    
    plan = OGEParallelPlan.query.get_or_404(plan_id)
    
    # Проверяем, что вебинар принадлежит этому плану
    plan_webinar = OGEParallelPlanWebinar.query.filter_by(
        plan_id=plan_id, 
        webinar_id=webinar_id
    ).first()
    
    if not plan_webinar:
        flash("Вебинар не найден в плане", "error")
        return redirect(url_for(".manage_oge_plan", plan_id=plan_id))
    
    # Проверяем, не отмечен ли уже как просмотренный
    existing = WatchedWebinar.query.filter_by(
        student_id=plan.student_id,
        webinar_id=webinar_id
    ).first()
    
    if existing:
        flash("Вебинар уже отмечен как просмотренный", "warning")
        return redirect(url_for(".manage_oge_plan", plan_id=plan_id))
    
    try:
        # Добавляем запись о просмотре
        watched_webinar = WatchedWebinar(
            student_id=plan.student_id,
            webinar_id=webinar_id,
            created_by_id=current_user.id
        )
        db.session.add(watched_webinar)
        db.session.commit()
        
        flash("Вебинар отмечен как просмотренный", "success")
        
    except Exception as e:
        flash(f"Ошибка при отметке вебинара: {str(e)}", "error")
    
    return redirect(url_for(".manage_oge_plan", plan_id=plan_id))


@bp.route("/oge/mark-all-webinars-watched/<int:plan_id>", methods=["POST"])
@login_required
def mark_all_oge_webinars_watched(plan_id):
    """Отметить все вебинары плана ОГЭ как просмотренные"""
    if current_user.is_educational_curator:
        abort(403)
    
    plan = OGEParallelPlan.query.get_or_404(plan_id)
    
    try:
        # Получаем все вебинары плана
        plan_webinars = plan.webinars
        
        # Получаем уже просмотренные вебинары
        watched_webinar_ids = {
            w.webinar_id for w in WatchedWebinar.query.filter_by(student_id=plan.student_id).all()
        }
        
        # Добавляем только непросмотренные вебинары
        added_count = 0
        for plan_webinar in plan_webinars:
            if plan_webinar.webinar_id not in watched_webinar_ids:
                watched_webinar = WatchedWebinar(
                    student_id=plan.student_id,
                    webinar_id=plan_webinar.webinar_id,
                    created_by_id=current_user.id
                )
                db.session.add(watched_webinar)
                added_count += 1
        
        db.session.commit()
        
        # Проверяем, это AJAX запрос или обычный
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': f'Отмечено как просмотренные: {added_count} вебинаров' if added_count > 0 else 'Все вебинары уже отмечены как просмотренные',
                'added_count': added_count
            })
        else:
            if added_count > 0:
                flash(f"Отмечено как просмотренные: {added_count} вебинаров", "success")
            else:
                flash("Все вебинары уже отмечены как просмотренные", "info")
            return redirect(url_for(".manage_oge_plan", plan_id=plan_id))
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': f'Ошибка при отметке вебинаров: {str(e)}'
            }), 500
        else:
            flash(f"Ошибка при отметке вебинаров: {str(e)}", "error")
            return redirect(url_for(".manage_oge_plan", plan_id=plan_id))


@bp.route("/oge/unmark-webinar-watched/<int:plan_id>/<int:webinar_id>", methods=["POST"])
@login_required
def unmark_oge_webinar_watched(plan_id, webinar_id):
    """Убрать отметку о просмотре вебинара в плане ОГЭ"""
    if current_user.is_educational_curator:
        abort(403)
    
    plan = OGEParallelPlan.query.get_or_404(plan_id)
    
    try:
        # Находим запись о просмотре
        watched_webinar = WatchedWebinar.query.filter_by(
            student_id=plan.student_id,
            webinar_id=webinar_id
        ).first()
        
        if watched_webinar:
            db.session.delete(watched_webinar)
            db.session.commit()
            flash("Отметка о просмотре вебинара убрана", "success")
        else:
            flash("Вебинар не был отмечен как просмотренный", "warning")
        
    except Exception as e:
        flash(f"Ошибка при снятии отметки: {str(e)}", "error")
    
    return redirect(url_for(".manage_oge_plan", plan_id=plan_id))
