from flask import render_template, request
from flask_login import login_required, current_user

from app.main import bp
from app.models import Student, Webinar, WebinarTask # Добавил WebinarTask

@bp.route('/')
@login_required
def index():
    # Шаблон будет искаться в app/templates/index.html
    return render_template("index.html")


@bp.route('/guide')
@login_required
def guide():
    # Шаблон будет искаться в app/templates/guide.html
    return render_template("guide.html")


@bp.route('/search')
@login_required
def search():
    query = request.args.get("q", "")
    students = [] # Инициализируем пустым списком по умолчанию
    webinars = []

    if not query:
        # Шаблон будет искаться в app/templates/search.html
        return render_template("search.html", results=None, query=None)

    # Поиск по ученикам (только если пользователь НЕ учебный куратор)
    if not current_user.is_educational_curator:
        students = Student.query.filter(
            (Student.first_name.ilike(f"%{query}%"))
            | (Student.last_name.ilike(f"%{query}%"))
            | (Student.platform_id.ilike(f"%{query}%"))
        ).all()

    # Поиск по вебинарам
    webinars_query = Webinar.query.filter(
        (
            Webinar.title.ilike(f"%{query}%")
            | Webinar.url.ilike(f"%{query}%")
            # Добавляем поиск по тексту задач, связанных с вебинаром
            | Webinar.tasks.any(WebinarTask.text.ilike(f"%{query}%")) 
        )
    )
    webinars = webinars_query.all()

    return render_template(
        "search.html", students=students, webinars=webinars, query=query
    )
