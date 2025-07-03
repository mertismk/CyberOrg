from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_, or_ # Импортируем and_, or_
import re # Импортируем re для обработки синонимов

from app.main import bp
from app.models import Student, Webinar, WebinarTask, WebinarComment, TaskNumber, StudyPlan # Исправил на StudyPlan

@bp.route('/')
@login_required
def index():
    # Получаем статистику для главной страницы
    students_count = Student.query.count() if not current_user.is_educational_curator else None
    webinars_count = Webinar.query.count()
    plans_count = StudyPlan.query.count()
    
    # Устанавливаем фиксированный учебный год
    current_academic_year = "2025-2026"
    
    # Выполняем поиск, если запрос был передан
    query = request.args.get("q", "").strip()
    search_results = None
    
    if query:
        # Используем существующую логику поиска
        search_results = perform_search(query)
    
    # Передаём статистику и результаты поиска в шаблон
    return render_template("index.html", 
                          students_count=students_count,
                          webinars_count=webinars_count,
                          plans_count=plans_count,
                          current_academic_year=current_academic_year,
                          search_results=search_results,
                          query=query)


@bp.route('/search-ajax')
@login_required
def search_ajax():
    """AJAX endpoint для поиска на главной странице"""
    query = request.args.get("q", "").strip()
    
    if not query:
        return jsonify({"students": [], "webinars": []})
    
    # Используем существующую логику поиска
    results = perform_search(query)
    
    return jsonify({
        "students": [{"id": s.id, "name": s.full_name, "platform_id": s.platform_id} for s in results["students"]],
        "webinars": [{"id": w.id, "title": w.title} for w in results["webinars"]]
    })


def perform_search(query):
    """Общая функция для поиска по ученикам и вебинарам"""
    students = []
    webinars = []

    if not query:
        return {"students": [], "webinars": []}

    # --- Обработка синонимов и чисел ---
    processed_query = query.lower() # Приводим к нижнему регистру для сравнения

    # Базовый словарь синонимов
    synonyms = {
        "сс": ["система счисления", "системы счисления"],
        "с.с.": ["система счисления", "системы счисления"],
        "систем счислени": ["система счисления", "системы счисления"], # Учитываем разные окончания
        "2й": ["второй", "вторая", "второе", "двоичной", "двоичная", "двоичное"],
        "втор": ["второй", "вторая", "второе", "двоичной", "двоичная", "двоичное", "2й"],
        "двоичн": ["второй", "вторая", "второе", "двоичной", "двоичная", "двоичное", "2й"],
    }

    query_variants = {processed_query}

    # Простая проверка на наличие ключей синонимов в запросе
    for key, values in synonyms.items():
        # Используем \\b для поиска целых слов/аббревиатур
        if re.search(r'\b' + re.escape(key) + r'\b', processed_query):
            query_variants.add(processed_query.replace(key, values[0])) # Добавляем основной синоним
            query_variants.update(values) # Добавляем все варианты из словаря
        # Проверяем, не содержится ли значение синонима в запросе
        for value in values:
             if re.search(r'\b' + re.escape(value) + r'\b', processed_query):
                 query_variants.add(key) # Добавляем ключ (например, "сс")
                 query_variants.update(values) # Добавляем остальные варианты

    # Преобразуем множество обратно в список для ilike
    search_terms = list(query_variants)

    # Разделяем исходный запрос на слова для поиска по И
    query_words = query.split()

    # --- Поиск по ученикам (теперь для всех пользователей) ---
    student_filters = []
    for term in search_terms: # Используем варианты запроса для поиска
        student_filters.append(Student.first_name.ilike(f"%{term}%"))
        student_filters.append(Student.last_name.ilike(f"%{term}%"))
        student_filters.append(Student.platform_id.ilike(f"%{term}%"))
    students = Student.query.filter(or_(*student_filters)).all()

    # --- Улучшенный поиск по вебинарам ---
    webinar_base_query = Webinar.query

    # Фильтр по отдельным словам
    webinar_word_filters = []
    for word in query_words:
        word_ilike = f"%{word}%"
        task_number_filter = None
        if word.isdigit():
             task_number_filter = Webinar.task_numbers.any(TaskNumber.number == int(word))

        word_conditions = [
            Webinar.title.ilike(word_ilike),
            Webinar.url.ilike(word_ilike),
            Webinar.tasks.any(WebinarTask.text.ilike(word_ilike)),
            Webinar.comments.any(WebinarComment.text.ilike(word_ilike)),
        ]
        if task_number_filter is not None:
             word_conditions.append(task_number_filter)

        webinar_word_filters.append(or_(*word_conditions))

    # Применяем фильтр по словам (все слова должны присутствовать)
    if webinar_word_filters:
        webinar_base_query = webinar_base_query.filter(and_(*webinar_word_filters))

    webinars = webinar_base_query.all()

    # --- Дополнительный поиск по синонимам (если основной поиск по словам не дал результатов или для расширения) ---
    if not webinars or True: # Пока всегда добавляем результаты по синонимам
        webinar_synonym_filters = []
        for term in search_terms: # Ищем по каждому варианту запроса
            term_ilike = f"%{term}%"
            task_number_filter = None
            # Проверка, является ли терм числом для поиска по номеру задания
            if term.isdigit():
                 task_number_filter = Webinar.task_numbers.any(TaskNumber.number == int(term))
            elif term.startswith("№") and term[1:].isdigit(): # Убираем № перед проверкой
                 task_number_filter = Webinar.task_numbers.any(TaskNumber.number == int(term[1:]))

            synonym_conditions = [
                 Webinar.title.ilike(term_ilike),
                 Webinar.url.ilike(term_ilike),
                 Webinar.tasks.any(WebinarTask.text.ilike(term_ilike)),
                 Webinar.comments.any(WebinarComment.text.ilike(term_ilike)),
            ]
            if task_number_filter is not None:
                synonym_conditions.append(task_number_filter)

            webinar_synonym_filters.append(or_(*synonym_conditions))

        # Ищем вебинары, которые подходят хотя бы под один из синонимов/вариантов
        if webinar_synonym_filters:
            synonym_webinars = Webinar.query.filter(or_(*webinar_synonym_filters)).all()
            # Объединяем результаты, избегая дубликатов
            webinar_ids = {w.id for w in webinars}
            for w in synonym_webinars:
                if w.id not in webinar_ids:
                    webinars.append(w)
                    webinar_ids.add(w.id)

    return {"students": students, "webinars": webinars}

@bp.route('/guide')
@login_required
def guide():
    # Шаблон будет искаться в app/templates/guide.html
    return render_template("guide.html")


@bp.route('/search')
@login_required
def search():
    # Для обратной совместимости оставляем этот маршрут,
    # но по сути он делает то же самое, что и главная страница с параметром q
    query = request.args.get("q", "").strip()
    results = perform_search(query)
    
    return render_template(
        "search.html", 
        students=results["students"], 
        webinars=results["webinars"], 
        query=query
    )
