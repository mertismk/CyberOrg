from flask import render_template, request
from flask_login import login_required

from app.main import bp
from app.models import Student, Webinar # Импортируем необходимые модели

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
    if not query:
        # Шаблон будет искаться в app/templates/search.html
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
        # Поиск по комментариям может быть ресурсоемким, возможно стоит убрать или оптимизировать
        # | (Webinar.comment.ilike(f"%{query}%")) # Webinar не имеет поля comment
    ).all()

    return render_template(
        "search.html", students=students, webinars=webinars, query=query
    )
