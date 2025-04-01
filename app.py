import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    abort,
)
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import pandas as pd
from datetime import datetime, timedelta
from functools import wraps
from models import (
    db,
    Webinar,
    Student,
    StudyPlan,
    PlannedWebinar,
    WatchedWebinar,
    KnownTaskNumber,
    TaskNumber,
    User,
    WebinarComment,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_key_for_cyberorg")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///cyberorg.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Инициализация базы данных
db.init_app(app)
migrate = Migrate(app, db)

# Инициализация менеджера авторизации
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите для доступа к этой странице."
login_manager.login_message_category = "warning"


# Обновление времени последнего доступа
@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.template_filter("yesno")
def yesno_filter(value):
    """Фильтр для преобразования булевого значения в текст Да/Нет."""
    if value:
        return "Да"
    return "Нет"


@app.template_filter("moscow_time")
def moscow_time_filter(date):
    """Фильтр для преобразования времени в московский формат."""
    if date is None:
        return "Не указано"

    if isinstance(date, datetime):
        # Добавляем 3 часа к UTC для перевода в московское время (UTC+3)
        moscow_time = date + timedelta(hours=3)
        # Формат с временем
        return moscow_time.strftime("%d.%m.%Y %H:%M (МСК)")
    else:
        # Формат только даты
        return date.strftime("%d.%m.%Y")


# Функция для проверки наличия обложки вебинара
@app.template_filter("webinar_cover_exists")
def webinar_cover_exists(webinar_id):
    cover_path = os.path.join(app.static_folder, "covers", f"{webinar_id}.png")
    return os.path.exists(cover_path)


# Декораторы для проверки прав доступа
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("У вас нет прав доступа к этой странице.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_super_admin:
            flash("У вас нет прав доступа к этой странице.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            # Проверяем, не является ли пароль стандартным
            if user.check_password("123456"):
                flash(
                    "Вы используете стандартный пароль. Пожалуйста, измените его в целях безопасности.",
                    "warning",
                )
                return redirect(url_for("profile"))

            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("index"))
        else:
            flash("Неверное имя пользователя или пароль.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из системы.", "success")
    return redirect(url_for("login"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

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
            return redirect(url_for("index"))

    # Проверяем, использует ли пользователь стандартный пароль
    is_default_password = current_user.check_password("123456")

    return render_template("profile.html", is_default_password=is_default_password)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/guide")
@login_required
def guide():
    return render_template("guide.html")


@app.route("/users")
@super_admin_required
def users_list():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/user/new", methods=["GET", "POST"])
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
            return redirect(url_for("user_new"))

        user = User(username=username, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Пользователь успешно создан!", "success")
        return redirect(url_for("users_list"))

    return render_template("user_form.html")


@app.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
@super_admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        role = request.form.get("role")
        password = request.form.get("password")

        user.role = role
        if password:
            user.set_password(password)

        db.session.commit()

        flash("Данные пользователя обновлены!", "success")
        return redirect(url_for("users_list"))

    return render_template("user_form.html", user=user)


@app.route("/students")
@login_required
def students_list():
    students = Student.query.all()
    return render_template("students.html", students=students)


@app.route("/student/<int:student_id>")
@login_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    study_plans = (
        StudyPlan.query.filter_by(student_id=student_id)
        .order_by(StudyPlan.created_at.desc())
        .all()
    )
    watched_webinars = WatchedWebinar.query.filter_by(student_id=student_id).all()
    known_tasks = KnownTaskNumber.query.filter_by(student_id=student_id).all()

    # Создаем список номеров заданий для более удобного использования в шаблоне
    known_task_numbers = [task.task_number for task in known_tasks]

    # Получаем список ID просмотренных вебинаров
    watched_webinar_ids = [w.webinar_id for w in watched_webinars]

    # Получаем все вебинары для ручного выбора
    webinars = Webinar.query.all()

    return render_template(
        "student_detail.html",
        student=student,
        study_plans=study_plans,
        watched_webinars=watched_webinars,
        known_tasks=known_tasks,
        known_task_numbers=known_task_numbers,
        watched_webinar_ids=watched_webinar_ids,
        webinars=webinars,
    )


@app.route("/student/new", methods=["GET", "POST"])
@login_required
def student_new():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        platform_id = request.form.get("platform_id")
        target_score = request.form.get("target_score")
        hours_per_week = request.form.get("hours_per_week")

        is_beginner = "is_beginner" in request.form
        knows_task_26 = "knows_task_26" in request.form
        knows_task_27 = "knows_task_27" in request.form

        student = Student(
            first_name=first_name,
            last_name=last_name,
            platform_id=platform_id,
            target_score=target_score if target_score else None,
            hours_per_week=hours_per_week if hours_per_week else None,
            is_beginner=is_beginner,
            knows_task_26=knows_task_26,
            knows_task_27=knows_task_27,
            created_by_id=current_user.id,
        )

        db.session.add(student)
        db.session.commit()

        flash("Ученик успешно добавлен!", "success")
        return redirect(url_for("student_detail", student_id=student.id))

    return render_template("student_form.html")


@app.route("/student/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def student_edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        student.first_name = request.form.get("first_name")
        student.last_name = request.form.get("last_name")
        student.platform_id = request.form.get("platform_id")
        student.target_score = request.form.get("target_score") or None
        student.hours_per_week = request.form.get("hours_per_week") or None

        student.is_beginner = "is_beginner" in request.form
        student.knows_task_26 = "knows_task_26" in request.form
        student.knows_task_27 = "knows_task_27" in request.form

        db.session.commit()

        flash("Данные ученика обновлены!", "success")
        return redirect(url_for("student_detail", student_id=student.id))

    return render_template("student_form.html", student=student)


@app.route("/webinars")
@login_required
def webinars_list():
    webinars = Webinar.query.all()
    return render_template("webinars.html", webinars=webinars)


@app.route("/search")
@login_required
def search():
    query = request.args.get("q", "")
    if not query:
        return render_template("search.html", results=None, query=None)

    # Поиск по ученикам
    students = Student.query.filter(
        (Student.first_name.ilike(f"%{query}%"))
        | (Student.last_name.ilike(f"%{query}%"))
        | (Student.platform_id.ilike(f"%{query}%"))
    ).all()

    # Поиск по вебинарам
    webinars = Webinar.query.filter(
        (Webinar.title.ilike(f"%{query}%"))
        | (Webinar.url.ilike(f"%{query}%"))
        | (Webinar.comment.ilike(f"%{query}%"))
    ).all()

    return render_template(
        "search.html", students=students, webinars=webinars, query=query
    )


@app.route("/student/<int:student_id>/plan/new", methods=["GET", "POST"])
@login_required
def create_study_plan(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        # Создаем новый план обучения
        study_plan = StudyPlan(student_id=student.id, created_by_id=current_user.id)
        db.session.add(study_plan)
        db.session.flush()  # Получаем ID плана до коммита

        # Получаем выбранные вебинары из формы
        webinar_ids = request.form.getlist("webinar_ids")
        week_numbers = request.form.getlist("week_numbers")

        for i, webinar_id in enumerate(webinar_ids):
            week_number = week_numbers[i] if i < len(week_numbers) else 1
            planned_webinar = PlannedWebinar(
                study_plan_id=study_plan.id,
                webinar_id=int(webinar_id),
                week_number=int(week_number),
            )
            db.session.add(planned_webinar)

        db.session.commit()

        flash("План обучения создан!", "success")
        return redirect(url_for("view_study_plan", plan_id=study_plan.id))

    # Получаем все вебинары
    webinars = Webinar.query.all()
    known_tasks = KnownTaskNumber.query.filter_by(student_id=student_id).all()
    known_task_numbers = [task.task_number for task in known_tasks]

    watched_webinar_ids = [
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=student_id).all()
    ]

    # Логика подбора вебинаров в зависимости от уровня и цели студента
    suitable_webinars = []

    # 1. Если студент начинающий - Python с нуля
    if student.is_beginner:
        beginner_webinars = [w for w in webinars if w.for_beginners]
        suitable_webinars.extend(beginner_webinars)

    # Подбираем задания в зависимости от целевого балла
    if student.target_score:
        # 60-70 баллов: задания 1-7, 9-12, 14, 16, 18, 19-21, 22
        if 60 <= student.target_score <= 70:
            tasks_needed = [
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
            ]
            for webinar in webinars:
                if (
                    webinar.task_numbers
                    and any(
                        task.number in tasks_needed for task in webinar.task_numbers
                    )
                    and webinar.for_basic
                ):
                    suitable_webinars.append(webinar)

        # 70-80 баллов: задания 1-12, 14, 16-23
        elif 70 < student.target_score <= 80:
            tasks_needed = list(range(1, 13)) + [14] + list(range(16, 24))
            for webinar in webinars:
                if (
                    webinar.task_numbers
                    and any(
                        task.number in tasks_needed for task in webinar.task_numbers
                    )
                    and webinar.for_basic
                ):
                    suitable_webinars.append(webinar)

        # 80-85 баллов: задания 1-23, 25
        elif 80 < student.target_score <= 85:
            tasks_needed = list(range(1, 24)) + [25]
            for webinar in webinars:
                if (
                    webinar.task_numbers
                    and any(
                        task.number in tasks_needed for task in webinar.task_numbers
                    )
                    and webinar.for_basic
                ):
                    suitable_webinars.append(webinar)

        # 85-90 баллов: задания 1-25
        elif 85 < student.target_score <= 90:
            tasks_needed = list(range(1, 26))
            for webinar in webinars:
                if (
                    webinar.task_numbers
                    and any(
                        task.number in tasks_needed for task in webinar.task_numbers
                    )
                    and webinar.for_basic
                ):
                    suitable_webinars.append(webinar)

        # 90-95 баллов: задания 1-25, 27
        elif 90 < student.target_score <= 95:
            tasks_needed = list(range(1, 26)) + [27]
            for webinar in webinars:
                if webinar.task_numbers and any(
                    task.number in tasks_needed for task in webinar.task_numbers
                ):
                    if webinar.for_basic or (
                        webinar.for_expert and not student.knows_task_27
                    ):
                        suitable_webinars.append(webinar)

        # 95-100 баллов: задания 1-27
        elif student.target_score > 95:
            tasks_needed = list(range(1, 28))
            for webinar in webinars:
                if webinar.task_numbers and any(
                    task.number in tasks_needed for task in webinar.task_numbers
                ):
                    suitable_webinars.append(webinar)

    # Удаляем дубликаты вебинаров, если они есть
    suitable_webinars = list(set(suitable_webinars))

    # Фильтруем уже просмотренные вебинары
    suitable_webinars = [
        w for w in suitable_webinars if w.id not in watched_webinar_ids
    ]

    # Исключаем вебинары, которые соответствуют только уже известным заданиям
    if known_task_numbers:
        suitable_webinars = [
            w
            for w in suitable_webinars
            if not (
                w.task_numbers
                and all(task.number in known_task_numbers for task in w.task_numbers)
            )
        ]

    # Расчет времени на вебинары
    # На 1 вебинар и ДЗ задания 1-25 по 3 часа, на 26 и 27 по 4 часа
    # Если ботает 26, то 30% времени на 26; если 27, то 30% на 27
    # Если оба, то по 25% на каждый
    total_hours_per_week = (
        student.hours_per_week or 9
    )  # По умолчанию 9 часов (3 вебинара)

    # Распределение времени на задания 26 и 27
    time_for_26_27 = 0

    # Для 90-95 баллов: 2 вебинара каждую неделю должны быть по заданию 27
    if 90 < student.target_score <= 95:
        time_for_26_27 = 8  # 2 вебинара по 4 часа
    # Для 95-100 баллов: 50-60% времени на 26 и 27 задания
    elif student.target_score > 95:
        time_for_26_27 = int(total_hours_per_week * 0.55)  # 55% времени на 26 и 27
    # Для других случаев используем стандартное распределение
    elif student.knows_task_26 and student.knows_task_27:
        # 50% времени на 26 и 27 (по 25% на каждый)
        time_for_26_27 = int(total_hours_per_week * 0.5)
    elif student.knows_task_26 or student.knows_task_27:
        # 30% времени на одно из заданий
        time_for_26_27 = int(total_hours_per_week * 0.3)

    # Оставшееся время на основные задания (1-25)
    time_for_basic = total_hours_per_week - time_for_26_27

    # Количество вебинаров в неделю для основных заданий
    basic_webinars_per_week = time_for_basic // 3

    # Количество вебинаров в неделю для заданий 26 и 27
    advanced_webinars_per_week = time_for_26_27 // 4

    # Общее количество вебинаров в неделю
    max_weekly_webinars = basic_webinars_per_week + advanced_webinars_per_week

    # Сортируем подходящие вебинары
    # Сначала по ID (чтобы соблюдать последовательность)
    suitable_webinars.sort(key=lambda w: w.id)

    # Разделяем вебинары на обычные (1-25) и продвинутые (26-27)
    basic_webinars = []
    advanced_webinars = []
    task27_cluster_webinars = []  # Вебинары по кластерам для задания 27
    task27_other_webinars = []  # Прочие вебинары для задания 27

    for webinar in suitable_webinars:
        # Пропускаем курс Python для начинающих, если галочка не стоит
        if webinar.for_beginners and not student.is_beginner:
            continue

        is_advanced = False
        is_task27_cluster = False

        if webinar.task_numbers:
            for task in webinar.task_numbers:
                if task.number == 27:
                    is_advanced = True
                    # Проверяем, относится ли вебинар к кластерам
                    if webinar.title and (
                        "кластер" in webinar.title.lower()
                        or "кластеры" in webinar.title.lower()
                    ):
                        is_task27_cluster = True
                    break
                elif task.number == 26:
                    is_advanced = True
                    break

        if is_advanced:
            if task.number == 27:
                if is_task27_cluster:
                    task27_cluster_webinars.append(webinar)
                else:
                    task27_other_webinars.append(webinar)
            else:
                advanced_webinars.append(webinar)
        else:
            basic_webinars.append(webinar)

    # Объединяем вебинары по заданию 27 с приоритетом кластеров
    task27_webinars = task27_cluster_webinars + task27_other_webinars
    advanced_webinars = task27_webinars + advanced_webinars

    # Общее количество вебинаров на 5 недель
    total_basic_webinars = basic_webinars_per_week * 5
    total_advanced_webinars = advanced_webinars_per_week * 5

    # Берем только необходимое количество вебинаров
    selected_basic_webinars = basic_webinars[:total_basic_webinars]
    selected_advanced_webinars = advanced_webinars[:total_advanced_webinars]

    # Объединяем выбранные вебинары
    final_webinars = selected_basic_webinars + selected_advanced_webinars

    # Распределяем вебинары по неделям
    webinar_weeks = {}

    # Для основных вебинаров (1-25)
    for i, webinar in enumerate(selected_basic_webinars):
        week = (i // basic_webinars_per_week) + 1
        if week > 5:
            week = 5
        webinar_weeks[webinar.id] = week

    # Для продвинутых вебинаров (26-27)
    for i, webinar in enumerate(selected_advanced_webinars):
        week = (i // advanced_webinars_per_week) + 1
        if week > 5:
            week = 5
        webinar_weeks[webinar.id] = week

    # Сортируем финальные вебинары по неделе и дате выхода
    final_webinars.sort(
        key=lambda w: (webinar_weeks.get(w.id, 5), w.date or datetime(2000, 1, 1))
    )

    # Проверяем, есть ли завершенные планы для этого студента
    last_plan = (
        StudyPlan.query.filter_by(student_id=student_id)
        .order_by(StudyPlan.created_at.desc())
        .first()
    )
    has_previous_plan = False

    if last_plan:
        # Проверяем, прошло ли 5 недель с момента создания последнего плана
        time_diff = datetime.utcnow() - last_plan.created_at
        if time_diff.days >= 35:  # приблизительно 5 недель
            has_previous_plan = True

    return render_template(
        "create_plan.html",
        student=student,
        webinars=webinars,
        suitable_webinars=final_webinars,
        known_task_numbers=known_task_numbers,
        watched_webinar_ids=watched_webinar_ids,
        max_weekly_webinars=max_weekly_webinars,
        webinar_weeks=webinar_weeks,
        has_previous_plan=has_previous_plan,
    )


@app.route("/plan/<int:plan_id>")
@login_required
def view_study_plan(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)

    # Организация вебинаров по неделям
    webinars_by_week = {}
    for planned in plan.planned_webinars:
        week = planned.week_number
        if week not in webinars_by_week:
            webinars_by_week[week] = []
        webinars_by_week[week].append(planned)

    # Сортировка вебинаров внутри каждой недели
    for week in webinars_by_week:
        webinars_by_week[week].sort(key=lambda x: x.webinar.id)

    # Сортировка недель
    weeks = {}
    for week in sorted(webinars_by_week.keys()):
        weeks[week] = webinars_by_week[week]

    # Список ID просмотренных вебинаров
    watched_webinar_ids = [
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=plan.student.id).all()
    ]
    
    # Получаем список известных заданий для студента
    known_tasks = KnownTaskNumber.query.filter_by(student_id=plan.student.id).all()
    known_task_numbers = [task.task_number for task in known_tasks]  # Убедимся, что это список чисел, а не объектов

    # Текущее время для отображения активной недели - используем полный datetime объект
    now = datetime.utcnow()

    return render_template(
        "view_plan.html",
        plan=plan,
        weeks=weeks,
        watched_webinar_ids=watched_webinar_ids,
        now=now,
        known_task_numbers=known_task_numbers,
    )


@app.route("/plan/<int:plan_id>/edit", methods=["GET", "POST"])
@login_required
def edit_study_plan(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    student = Student.query.get(plan.student_id)

    if request.method == "POST":
        # Удаляем все запланированные вебинары из этого плана
        PlannedWebinar.query.filter_by(study_plan_id=plan.id).delete()

        # Получаем выбранные вебинары из формы
        webinar_ids = request.form.getlist("webinar_ids")
        week_numbers = request.form.getlist("week_numbers")

        for i, webinar_id in enumerate(webinar_ids):
            week_number = week_numbers[i] if i < len(week_numbers) else 1
            planned_webinar = PlannedWebinar(
                study_plan_id=plan.id,
                webinar_id=int(webinar_id),
                week_number=int(week_number),
            )
            db.session.add(planned_webinar)

        db.session.commit()

        flash("План обучения обновлен!", "success")
        return redirect(url_for("view_study_plan", plan_id=plan.id))

    # Получаем текущие вебинары в плане
    current_planned_webinars = PlannedWebinar.query.filter_by(
        study_plan_id=plan.id
    ).all()

    # Получаем все вебинары
    webinars = Webinar.query.all()
    known_tasks = KnownTaskNumber.query.filter_by(student_id=student.id).all()
    known_task_numbers = [task.task_number for task in known_tasks]

    watched_webinar_ids = [
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=student.id).all()
    ]

    # Создаем словарь с текущими неделями для каждого вебинара
    webinar_weeks = {pw.webinar_id: pw.week_number for pw in current_planned_webinars}

    # Расчет времени для распределения вебинаров
    total_hours_per_week = (
        student.hours_per_week or 9
    )  # По умолчанию 9 часов (3 вебинара)

    # Распределение времени на задания 26 и 27
    time_for_26_27 = 0
    if student.knows_task_26 and student.knows_task_27:
        # 50% времени на 26 и 27 (по 25% на каждый)
        time_for_26_27 = int(total_hours_per_week * 0.5)
    elif student.knows_task_26 or student.knows_task_27:
        # 30% времени на одно из заданий
        time_for_26_27 = int(total_hours_per_week * 0.3)

    # Оставшееся время на основные задания (1-25)
    time_for_basic = total_hours_per_week - time_for_26_27

    # Количество вебинаров в неделю для основных заданий
    basic_webinars_per_week = time_for_basic // 3

    # Количество вебинаров в неделю для заданий 26 и 27
    advanced_webinars_per_week = time_for_26_27 // 4

    # Общее количество вебинаров в неделю
    max_weekly_webinars = basic_webinars_per_week + advanced_webinars_per_week

    return render_template(
        "edit_plan.html",
        plan=plan,
        student=student,
        webinars=webinars,
        current_planned_webinars=current_planned_webinars,
        known_task_numbers=known_task_numbers,
        watched_webinar_ids=watched_webinar_ids,
        webinar_weeks=webinar_weeks,
        max_weekly_webinars=max_weekly_webinars,
    )


@app.route("/student/<int:student_id>/watched", methods=["POST"])
@login_required
def mark_webinar_watched(student_id):
    action = request.form.get("action")

    if action == "unwatch":
        # Удаление вебинара из просмотренных
        webinar_id = request.form.get("webinar_id")
        watched = WatchedWebinar.query.filter_by(
            student_id=student_id, webinar_id=webinar_id
        ).first()
        if watched:
            db.session.delete(watched)
            db.session.commit()
            flash("Вебинар удален из просмотренных", "success")
        return redirect(url_for("student_detail", student_id=student_id))

    elif action == "add_by_links":
        # Добавление вебинаров по ссылкам
        webinar_links = request.form.get("webinar_links", "").strip().split("\n")
        added_count = 0
        not_found = []

        for link in webinar_links:
            link = link.strip()
            if not link:
                continue

            webinar = Webinar.query.filter_by(url=link).first()
            if webinar:
                # Проверяем, не отмечен ли уже этот вебинар
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
            else:
                not_found.append(link)

        db.session.commit()

        if added_count > 0:
            flash(f"Успешно добавлено {added_count} вебинаров", "success")
        if not_found:
            flash(
                f"Не найдены вебинары со следующими ссылками:\n" + "\n".join(not_found),
                "warning",
            )

        return redirect(url_for("student_detail", student_id=student_id))

    elif action == "add_manual":
        # Добавление вебинаров через ручной выбор
        webinar_ids = request.form.getlist("webinar_ids")
        added_count = 0

        for webinar_id in webinar_ids:
            # Проверяем, не отмечен ли уже этот вебинар
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

        db.session.commit()

        if added_count > 0:
            flash(f"Успешно добавлено {added_count} вебинаров", "success")

        return redirect(url_for("student_detail", student_id=student_id))

    else:
        # Оригинальная логика для одиночного вебинара
        webinar_id = request.form.get("webinar_id")

        # Проверяем, не отмечен ли уже этот вебинар как просмотренный
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
            db.session.commit()

            # После отметки вебинара как просмотренного, проверяем,
            # есть ли номера заданий, для которых просмотрены все вебинары
            webinar = Webinar.query.get(webinar_id)
            if webinar and webinar.task_numbers:
                for task in webinar.task_numbers:
                    task_webinars = task.webinars
                    watched_webinar_ids = [
                        w.webinar_id
                        for w in WatchedWebinar.query.filter_by(
                            student_id=student_id
                        ).all()
                    ]

                    all_watched = True
                    for tw in task_webinars:
                        if tw.id not in watched_webinar_ids:
                            all_watched = False
                            break

                    if all_watched:
                        existing_task = KnownTaskNumber.query.filter_by(
                            student_id=student_id, task_number=task.number
                        ).first()

                        if not existing_task:
                            known_task = KnownTaskNumber(
                                student_id=student_id, task_number=task.number
                            )
                            db.session.add(known_task)
                            db.session.commit()
                            flash(
                                f"Задание №{task.number} автоматически отмечено как изученное",
                                "success",
                            )

            flash("Вебинар отмечен как просмотренный", "success")
        else:
            flash("Этот вебинар уже отмечен как просмотренный", "warning")

        return redirect(url_for("student_detail", student_id=student_id))


@app.route("/student/<int:student_id>/tasks", methods=["POST"])
@login_required
def update_known_tasks(student_id):
    known_task_ids = request.form.getlist("known_tasks")

    # Удаляем все текущие задания для студента
    KnownTaskNumber.query.filter_by(student_id=student_id).delete()

    # Добавляем новые задания
    for task_id in known_task_ids:
        known_task = KnownTaskNumber(student_id=student_id, task_number=int(task_id))
        db.session.add(known_task)

    db.session.commit()
    flash("Список известных заданий обновлен", "success")

    return redirect(url_for("student_detail", student_id=student_id))


@app.route("/import_webinars", methods=["GET", "POST"])
@login_required
def import_webinars():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Файл не выбран", "error")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("Файл не выбран", "error")
            return redirect(request.url)

        if not file.filename.endswith((".xlsx", ".xls")):
            flash("Поддерживаются только Excel файлы (.xlsx, .xls)", "error")
            return redirect(request.url)

        try:
            # Читаем Excel файл
            df = pd.read_excel(file)

            # Проверяем обязательные колонки
            required_columns = ["название вебинара", "ссылка на вебинар"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                flash(
                    f'Отсутствуют обязательные колонки: {", ".join(missing_columns)}',
                    "error",
                )
                return redirect(request.url)

            # Счетчики для статистики
            total_rows = len(df)
            imported_count = 0
            errors = []

            for index, row in df.iterrows():
                try:
                    # Проверяем обязательные поля
                    if pd.isna(row["название вебинара"]) or pd.isna(
                        row["ссылка на вебинар"]
                    ):
                        errors.append(
                            f"Строка {index + 2}: Отсутствуют обязательные поля"
                        )
                        continue

                    # Создаем вебинар
                    webinar = Webinar(
                        title=str(row["название вебинара"]),
                        url=str(row["ссылка на вебинар"]),
                        created_by_id=current_user.id,
                    )

                    # Обрабатываем опциональные поля
                    if "дата вебинара" in df.columns and not pd.isna(
                        row["дата вебинара"]
                    ):
                        try:
                            webinar.date = pd.to_datetime(row["дата вебинара"]).date()
                        except:
                            errors.append(f"Строка {index + 2}: Неверный формат даты")

                    if "номера заданий" in df.columns and not pd.isna(
                        row["номера заданий"]
                    ):
                        task_numbers = str(row["номера заданий"]).split(",")
                        for task_num in task_numbers:
                            try:
                                num = int(task_num.strip())
                                task = TaskNumber.query.filter_by(number=num).first()
                                if not task:
                                    task = TaskNumber(number=num)
                                    db.session.add(task)
                                webinar.task_numbers.append(task)
                            except ValueError:
                                errors.append(
                                    f"Строка {index + 2}: Неверный формат номера задания: {task_num}"
                                )

                    if "решение прогой или руки" in df.columns and not pd.isna(
                        row["решение прогой или руки"]
                    ):
                        solution_type = str(row["решение прогой или руки"]).lower()
                        webinar.is_programming = "прогой" in solution_type
                        webinar.is_manual = "руками" in solution_type

                    if "номер дз" in df.columns and not pd.isna(row["номер дз"]):
                        try:
                            webinar.homework_number = int(row["номер дз"])
                        except ValueError:
                            errors.append(
                                f"Строка {index + 2}: Неверный формат номера ДЗ"
                            )

                    if "категория" in df.columns and not pd.isna(row["категория"]):
                        try:
                            webinar.category = int(row["категория"])
                            if webinar.category not in [1, 2, 3]:
                                errors.append(
                                    f"Строка {index + 2}: Неверное значение категории"
                                )
                        except ValueError:
                            errors.append(
                                f"Строка {index + 2}: Неверный формат категории"
                            )

                    if "категория курса" in df.columns and not pd.isna(
                        row["категория курса"]
                    ):
                        course_category = str(row["категория курса"]).lower()
                        webinar.for_beginners = "python с нуля" in course_category
                        webinar.for_basic = "основной курс" in course_category
                        webinar.for_advanced = "хард прога" in course_category
                        webinar.for_expert = "задание 27" in course_category

                    if "комментарий" in df.columns and not pd.isna(row["комментарий"]):
                        comment = WebinarComment(
                            text=str(row["комментарий"]),
                            webinar=webinar,
                            user_id=current_user.id,
                            created_at=datetime.utcnow(),  # Явно устанавливаем дату создания
                        )
                        db.session.add(comment)

                    if "ссылка на обложку" in df.columns and not pd.isna(
                        row["ссылка на обложку"]
                    ):
                        webinar.cover_url = str(row["ссылка на обложку"])

                    db.session.add(webinar)
                    imported_count += 1

                except Exception as e:
                    errors.append(f"Строка {index + 2}: {str(e)}")

            if errors:
                db.session.rollback()
                flash(f"Ошибки при импорте:\n" + "\n".join(errors), "error")
            else:
                db.session.commit()
                flash(
                    f"Успешно импортировано {imported_count} из {total_rows} вебинаров",
                    "success",
                )

            return redirect(url_for("webinars_list"))

        except Exception as e:
            flash(f"Ошибка при чтении файла: {str(e)}", "error")
            return redirect(request.url)

    return render_template("import_webinars.html")


# Новый маршрут для удаления плана
@app.route("/plan/<int:plan_id>/delete", methods=["POST"])
@login_required
def delete_study_plan(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    student_id = plan.student_id

    # Проверяем права доступа (только админы или создатель)
    if not current_user.is_admin and plan.created_by_id != current_user.id:
        flash("У вас нет прав на удаление этого плана.", "danger")
        return redirect(url_for("student_detail", student_id=student_id))

    # Удаляем все связанные запланированные вебинары
    PlannedWebinar.query.filter_by(study_plan_id=plan.id).delete()

    # Удаляем сам план
    db.session.delete(plan)
    db.session.commit()

    flash("План обучения успешно удален!", "success")
    return redirect(url_for("student_detail", student_id=student_id))


# Новый маршрут для массовой отметки вебинаров как просмотренных
@app.route("/plan/<int:plan_id>/mark_all_watched", methods=["POST"])
@login_required
def mark_all_webinars_watched(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)

    # Проверяем, что пользователь имеет право отмечать вебинары
    # (администратор или создатель плана)
    if not current_user.is_admin and current_user.id != plan.created_by_id:
        flash("У вас нет прав для выполнения этого действия", "danger")
        return redirect(url_for("view_study_plan", plan_id=plan_id))

    # Получаем все запланированные вебинары из плана
    planned_webinars = PlannedWebinar.query.filter_by(study_plan_id=plan_id).all()
    webinar_ids = [pw.webinar_id for pw in planned_webinars]

    # Отмечаем все вебинары как просмотренные, если они еще не отмечены
    watched_count = 0
    for webinar_id in webinar_ids:
        existing = WatchedWebinar.query.filter_by(
            student_id=plan.student_id, webinar_id=webinar_id
        ).first()

        if not existing:
            watched = WatchedWebinar(
                student_id=plan.student_id,
                webinar_id=webinar_id,
                created_by_id=current_user.id,
            )
            db.session.add(watched)
            watched_count += 1

    db.session.commit()

    # Проверяем для каждого задания, все ли вебинары просмотрены
    # Получаем просмотренные вебинары этого ученика
    watched_webinar_ids = [
        w.webinar_id
        for w in WatchedWebinar.query.filter_by(student_id=plan.student_id).all()
    ]

    # Получаем все номера заданий из просмотренных вебинаров
    task_numbers = set()
    for webinar_id in webinar_ids:
        webinar = Webinar.query.get(webinar_id)
        if webinar and webinar.task_numbers:
            for task in webinar.task_numbers:
                task_numbers.add(task)

    # Для каждого номера заданий проверяем, все ли вебинары просмотрены
    tasks_marked = 0
    for task in task_numbers:
        # Получаем все вебинары по этому номеру задания
        task_webinars = task.webinars

        # Проверяем, все ли вебинары по этому заданию просмотрены
        all_watched = True
        for tw in task_webinars:
            if tw.id not in watched_webinar_ids:
                all_watched = False
                break

        # Если все вебинары просмотрены, отмечаем задание как изученное
        if all_watched:
            # Проверяем, не отмечено ли уже это задание
            existing_task = KnownTaskNumber.query.filter_by(
                student_id=plan.student_id, task_number=task.number
            ).first()

            if not existing_task:
                known_task = KnownTaskNumber(
                    student_id=plan.student_id, task_number=task.number
                )
                db.session.add(known_task)
                tasks_marked += 1

    if tasks_marked > 0:
        db.session.commit()
        flash(f"{tasks_marked} заданий автоматически отмечены как изученные", "success")

    if watched_count > 0:
        flash(f"{watched_count} вебинаров отмечены как просмотренные", "success")
    else:
        flash("Все вебинары уже были отмечены ранее", "info")

    return redirect(url_for("view_study_plan", plan_id=plan_id))


@app.route("/webinar/<int:webinar_id>/comment", methods=["POST"])
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

    return redirect(url_for("webinars_list"))


@app.route("/webinar/comment/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_webinar_comment(comment_id):
    comment = WebinarComment.query.get_or_404(comment_id)

    # Проверяем права на удаление
    if current_user.id != comment.user_id and not current_user.is_admin:
        abort(403)

    webinar_id = comment.webinar_id
    db.session.delete(comment)
    db.session.commit()

    flash("Комментарий успешно удален", "success")
    return redirect(url_for("webinars_list"))


# Обработка ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Обработка ошибки 403
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


# Инициализация базы данных и создание стандартных пользователей
@app.cli.command("init-db")
def init_db_command():
    """Инициализация базы данных начальными данными."""
    # Создаем номера заданий
    for i in range(1, 28):
        task = TaskNumber.query.filter_by(number=i).first()
        if not task:
            task = TaskNumber(number=i)
            db.session.add(task)

    # Создаем пользователей
    users_data = [
        {
            "username": "makarkonev",
            "role": "super_admin",
            "first_name": "Макар",
            "last_name": "Конев",
        },
        {
            "username": "katherinevstheworld",
            "role": "super_admin",
            "first_name": "Катерина",
            "last_name": "Бриль",
        },
        {
            "username": "zinger_s",
            "role": "admin",
            "first_name": "Александра",
            "last_name": "Смирнова",
        },
        {
            "username": "firstdarksoul",
            "role": "admin",
            "first_name": "Максим",
            "last_name": "Михеев",
        },
        {
            "username": "velukayataina",
            "role": "admin",
            "first_name": "Таина",
            "last_name": "Житина",
        },
        {
            "username": "mkhorinova",
            "role": "regular",
            "first_name": "Муслима",
            "last_name": "Хоринова",
        },
        {
            "username": "pollliin",
            "role": "regular",
            "first_name": "Полина",
            "last_name": "Гусева",
        },
        {
            "username": "lllsbp",
            "role": "regular",
            "first_name": "Самира",
            "last_name": "Шигалугова",
        },
        {
            "username": "elya_na_svyazi",
            "role": "regular",
            "first_name": "Элина",
            "last_name": "Аметова",
        },
        {
            "username": "arr_niga",
            "role": "regular",
            "first_name": "Артём",
            "last_name": "Нигматулин",
        },
        {
            "username": "dariashupikova",
            "role": "regular",
            "first_name": "Дарья",
            "last_name": "Шупикова",
        },
        {
            "username": "amalia_m_21",
            "role": "regular",
            "first_name": "Амалия",
            "last_name": "Мордвинова",
        },
    ]

    for user_data in users_data:
        username = user_data["username"]
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(
                username=username,
                role=user_data["role"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
            )
            user.set_password(
                "123456"
            )  # Стандартный пароль для всех новых пользователей
            db.session.add(user)

    db.session.commit()
    print("База данных успешно инициализирована!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
