from datetime import datetime, date
import re
from collections import deque, Counter  # Добавляем Counter

# Переносим импорт сюда
from app import db
from app.models import Webinar  # Добавляем этот импорт


def get_webinar_hours(webinar: Webinar) -> float:
    """Определяет "стоимость" вебинара в часах."""
    # Особые случаи для конкретных вебинаров
    if webinar.id in [17, 33]:
        return 0.3

    if webinar.for_beginners:
        return 2.5
    elif (
        webinar.for_advanced or webinar.for_expert
    ):  # Считаем, что это T26/T27 для целей часов
        # Используем константу
        return 4.0
    # По умолчанию (включая for_basic, for_mocks, for_practice, for_minisnap и без флагов)
    return 3.0


# --- Вспомогательные функции для сортировки ---
def get_priority_for_webinar(webinar):
    # Новые приоритеты: 0=Кат_1, 1=Кат_2, 2=Кат_4, 3=Кат_3, 4=Другие
    if not webinar:
        return 4  # Самый низкий

    # Убираем специальную логику для T26/T27, приоритет теперь ТОЛЬКО по категории
    # if webinar.for_advanced or webinar.for_expert:
    #    return 0

    category = webinar.category
    if category == 1:
        return 0  # Обязательный
    elif category == 2:
        return 1  # Повторение
    elif category == 4:
        return 2  # Продвинутый (ПОЛЬЗОВАТЕЛЬСКИЙ ПОРЯДОК)
    elif category == 3:
        return 3  # Не обязательный (ПОЛЬЗОВАТЕЛЬСКИЙ ПОРЯДОК)
    else:
        return 4  # Остальные/Без категории


def get_sortable_datetime(webinar_date):
    dt_obj = None
    if webinar_date:
        if isinstance(webinar_date, datetime):
            dt_obj = webinar_date
        elif isinstance(webinar_date, date):
            dt_obj = datetime.combine(webinar_date, datetime.min.time())
    # Сортируем: сначала с датой (0), потом без даты (1); затем по самой дате
    if dt_obj:
        return (0, dt_obj.replace(tzinfo=None))
    # Ставим очень давнюю дату для вебинаров без даты, чтобы они были последними
    return (1, datetime(1970, 1, 1))


def create_webinar_sort_key(webinar):
    """Создает ключ для сортировки вебинаров: Категория -> Дата -> ID."""
    return (
        get_priority_for_webinar(webinar),
        get_sortable_datetime(webinar.date),
        webinar.id,
    )


# --- Новые вспомогательные функции ---

def _extract_beginner_lesson_number(title: str) -> int:
    """Пытается извлечь номер занятия из названия ролика. Если не найдено — возвращает большое число.

    Ожидаемые форматы: "Занятие 1", "Урок 2", просто число в названии.
    """
    if not title:
        return 10_000
    # Ищем конструкции вида "Занятие 12" или "Урок 5"
    match = re.search(r"(?:занятие|урок)\s*(\d+)", title, flags=re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    # Иначе берём первое число в названии, если есть
    any_num = re.search(r"(\d+)", title)
    if any_num:
        try:
            return int(any_num.group(1))
        except ValueError:
            pass
    return 10_000

def _beginner_sort_key(webinar: Webinar):
    """Ключ сортировки для роликов Python с нуля: по номеру занятия, затем по дате, затем по ID."""
    number = _extract_beginner_lesson_number(getattr(webinar, 'title', '') or '')
    # Для стабильности сортируем дальше по дате и ID
    dt_key = get_sortable_datetime(getattr(webinar, 'date', None))
    return (number, dt_key, webinar.id)

def analyze_webinar_blocks(webinars, watched_webinar_ids, hours_per_week=9, needs_python_basics=False, is_first_plan=True, needs_task_26=False, include_2025_webinars=False):
    """
    Анализирует вебинары и группирует их по блокам с учетом новых требований.
    
    Args:
        webinars: список вебинаров
        watched_webinar_ids: множество ID просмотренных вебинаров
        hours_per_week: количество часов в неделю
        needs_python_basics: нужен ли Python с нуля
        is_first_plan: является ли это первым планом
        needs_task_26: нужно ли задание 26
        include_2025_webinars: включать ли вебинары 2024-2025 года
    
    Returns:
        dict: Словарь с информацией о блоках вебинаров
    """
    blocks = {
        'beginners': {'count': 0, 'hours': 0, 'recommended_per_week': 0},
        'basic': {'count': 0, 'hours': 0, 'recommended_per_week': 0},
        'advanced': {'count': 0, 'hours': 0, 'recommended_per_week': 0},
        'mocks': {'count': 0, 'hours': 0, 'recommended_per_week': 0},
        'practice': {'count': 0, 'hours': 0, 'recommended_per_week': 0},
        'minisnap': {'count': 0, 'hours': 0, 'recommended_per_week': 0},
    }
    
    for webinar in webinars:
        if webinar.id in watched_webinar_ids:
            continue
            
        # Исключаем мини-щелчок для вебинаров 2024-2025 года
        if webinar.for_minisnap and not include_2025_webinars and webinar.academic_year == 2025:
            continue
            
        webinar_hours = get_webinar_hours(webinar)
        
        if webinar.for_beginners:
            blocks['beginners']['count'] += 1
            blocks['beginners']['hours'] += webinar_hours
        elif webinar.for_basic or webinar.for_expert:  # T27 теперь входит в основной курс
            blocks['basic']['count'] += 1
            blocks['basic']['hours'] += webinar_hours
        elif webinar.for_advanced:  # T26
            blocks['advanced']['count'] += 1
            blocks['advanced']['hours'] += webinar_hours
        elif webinar.for_mocks:
            blocks['mocks']['count'] += 1
            blocks['mocks']['hours'] += webinar_hours
        elif webinar.for_practice:
            blocks['practice']['count'] += 1
            blocks['practice']['hours'] += webinar_hours
        elif webinar.for_minisnap:
            blocks['minisnap']['count'] += 1
            blocks['minisnap']['hours'] += webinar_hours
    
    # Рассчитываем рекомендуемые значения на неделю согласно новым требованиям
    for block_key, block_data in blocks.items():
        if block_data['count'] > 0:
            avg_hours_per_webinar = block_data['hours'] / block_data['count']
            
            # Определяем процент времени для блока
            time_percentage = 0.0
            
            if block_key == 'beginners' and needs_python_basics:
                time_percentage = 0.66  # 66% времени на Python с нуля
            elif block_key == 'basic':
                if needs_python_basics:
                    time_percentage = 0.34  # 34% времени на основной курс (если есть Python)
                elif needs_task_26:
                    time_percentage = 0.66  # 66% времени на основной курс (если есть T26)
                else:
                    time_percentage = 1.0   # 100% времени на основной курс
            elif block_key == 'advanced' and needs_task_26 and not needs_python_basics:
                time_percentage = 0.34  # 34% времени на T26
            else:
                # Для остальных блоков (mocks, practice, minisnap) - минимальное время
                time_percentage = 0.1
            
            # Рассчитываем количество вебинаров на основе процента времени
            max_webinars_by_hours = int(hours_per_week * time_percentage / avg_hours_per_webinar)
            
            # Берем минимум из расчета по часам и общего количества вебинаров
            block_data['recommended_per_week'] = min(max_webinars_by_hours, block_data['count'])
            
            # Минимум 1 вебинар в неделю, если есть вебинары в блоке и он нужен
            if block_data['recommended_per_week'] == 0 and block_data['count'] > 0:
                if (block_key == 'beginners' and needs_python_basics) or \
                   (block_key == 'basic') or \
                   (block_key == 'advanced' and needs_task_26 and not needs_python_basics):
                    block_data['recommended_per_week'] = 1
        else:
            block_data['recommended_per_week'] = 0
    
    return blocks


def _filter_webinars_by_block_quotas(webinars, block_quotas, watched_webinar_ids, hours_per_week=15):
    """
    Фильтрует вебинары по квотам блоков и распределяет их по неделям.
    
    Args:
        webinars: список всех вебинаров
        block_quotas: словарь с квотами блоков {'beginners': 3, 'basic': 1, ...}
        watched_webinar_ids: множество ID просмотренных вебинаров
        hours_per_week: максимум часов в неделю
    
    Returns:
        tuple: (filtered_webinars, webinar_weeks)
    """
    filtered_webinars = []
    webinar_weeks = {}
    
    # Группируем вебинары по блокам
    webinars_by_block = {
        'beginners': [],
        'basic': [],
        'advanced': [],
        'mocks': [],
        'practice': [],
        'minisnap': []
    }
    
    for webinar in webinars:
        if webinar.id in watched_webinar_ids:
            continue
            
        # Определяем к какому блоку относится вебинар
        block_key = None
        if webinar.for_beginners:
            block_key = 'beginners'
        elif webinar.for_basic or webinar.for_expert:  # T27 теперь входит в основной курс
            block_key = 'basic'
        elif webinar.for_advanced:  # T26
            block_key = 'advanced'
        elif webinar.for_mocks:
            block_key = 'mocks'
        elif webinar.for_practice:
            block_key = 'practice'
        elif webinar.for_minisnap:
            block_key = 'minisnap'
        
        if block_key:
            webinars_by_block[block_key].append(webinar)
    
    # Сортируем вебинары в каждом блоке: beginner по номеру занятия, остальные по дате
    for block_key, block_webinars in webinars_by_block.items():
        if block_key == 'beginners':
            block_webinars.sort(key=_beginner_sort_key)
        else:
            block_webinars.sort(key=lambda w: w.date if w.date else datetime.min.date())
    
    # Распределяем вебинары по неделям согласно квотам (каждую неделю)
    print(f"Block quotas applied - distributing webinars (per week):")
    
    # Трекер часов по неделям
    weekly_hours = {week: 0.0 for week in range(1, 5)}
    
    for week in range(1, 5):  # 4 недели
        for block_key, quota_per_week in block_quotas.items():
            if quota_per_week <= 0:
                continue
                
            block_webinars = webinars_by_block[block_key]
            selected_count = 0
            
            # Выбираем вебинары согласно квоте, но не превышая лимит часов
            for webinar in block_webinars:
                if webinar.id in webinar_weeks:  # Уже назначен
                    continue
                    
                if selected_count >= quota_per_week:
                    break
                    
                webinar_hours = get_webinar_hours(webinar)
                if weekly_hours[week] + webinar_hours <= hours_per_week:
                    filtered_webinars.append(webinar)
                    webinar_weeks[webinar.id] = week
                    weekly_hours[week] += webinar_hours
                    selected_count += 1
                else:
                    print(f"  Week {week}, {block_key}: webinar {webinar.id} skipped - would exceed hour limit")
            
            if selected_count > 0:
                print(f"  Week {week}, {block_key}: {selected_count} webinars selected ({weekly_hours[week]:.1f}h total)")
    
    # Дозаполняем недели до лимита часов вебинарами основного курса
    print("\nFilling remaining hours with basic course webinars:")
    basic_webinars = webinars_by_block.get('basic', [])
    
    for week in range(1, 5):
        remaining_hours = hours_per_week - weekly_hours[week]
        if remaining_hours > 1.0:  # Если остается больше 1 часа
            print(f"  Week {week}: {remaining_hours:.1f}h remaining, adding basic webinars...")
            added_count = 0
            
            for webinar in basic_webinars:
                if webinar.id in webinar_weeks:  # Уже назначен
                    continue
                    
                webinar_hours = get_webinar_hours(webinar)
                if weekly_hours[week] + webinar_hours <= hours_per_week:
                    filtered_webinars.append(webinar)
                    webinar_weeks[webinar.id] = week
                    weekly_hours[week] += webinar_hours
                    added_count += 1
                    print(f"    Added webinar {webinar.id} ({webinar_hours:.1f}h), total: {weekly_hours[week]:.1f}h")
                    
                    # Если осталось мало времени, останавливаемся
                    if hours_per_week - weekly_hours[week] < 1.0:
                        break
            
            if added_count > 0:
                print(f"  Week {week}: added {added_count} basic webinars, final: {weekly_hours[week]:.1f}h")
    
    # Подсчитываем общее количество по блокам
    block_totals = {}
    for webinar in filtered_webinars:
        for block_key, block_webinars in webinars_by_block.items():
            if webinar in block_webinars:
                block_totals[block_key] = block_totals.get(block_key, 0) + 1
                break
    
    print(f"Total webinars selected by block: {block_totals}")
    return filtered_webinars, webinar_weeks


def _handle_beginner_webinars(
    student, all_webinars, watched_webinar_ids, hours_per_week, videos_per_week: int = 3, weeks: int = 4
):
    """Обрабатывает вебинары 'Python с нуля' и раскладывает ровно по videos_per_week на неделю по порядку.

    Возвращает список выбранных роликов и маппинг ID -> неделя, а также набор назначенных ID.
    """
    selected_beginner_webinars = []
    beginner_weeks = {}
    beginner_assigned_ids = set()

    if student.needs_python_basics:
        beginner_webinars_available = [
            w
            for w in all_webinars
            if w.for_beginners and w.id not in watched_webinar_ids
        ]
        beginner_webinars_available.sort(key=_beginner_sort_key)
        print(
            f"\nНайдено доступных beginner вебинаров: {len(beginner_webinars_available)}"
        )

        # Берём по videos_per_week на каждую неделю, максимум на 'weeks' недель
        max_videos = videos_per_week * weeks
        sliced = beginner_webinars_available[:max_videos]
        for idx, w in enumerate(sliced):
            week_number = (idx // videos_per_week) + 1  # 1..weeks
            if week_number > weeks:
                break
            selected_beginner_webinars.append(w)
            beginner_assigned_ids.add(w.id)
            beginner_weeks[w.id] = week_number

        # Выведем статистику по неделям
        per_week_counts = {wn: 0 for wn in range(1, weeks + 1)}
        for wid, wn in beginner_weeks.items():
            per_week_counts[wn] += 1
        for wn in range(1, weeks + 1):
            print(f"Добавлено beginner (Неделя {wn}): {per_week_counts[wn]} вебинаров ({per_week_counts[wn] * 2.5:.1f} часов)")
    else:
        print("\nPython Basics не требуется.")

    return (
        selected_beginner_webinars,
        beginner_weeks,
        beginner_assigned_ids,
    )


def _determine_required_tasks(
    student, known_task_numbers, is_first_plan
):
    """Определяет необходимые задания с учетом балла, известных и логики откладывания."""
    required_tasks = set()
    # Определяем базовый набор заданий по целевому баллу/оценке
    target_score = (
        student.target_score or 85
    )  # Используем 85 как дефолт, если не указано
    
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
        tasks_70_80 = set(range(1, 13)) | {14} | set(range(16, 24))  # 1-12, 14, 16-23
        tasks_80_85 = set(range(1, 24)) | {25}  # 1-23, 25
        tasks_85_90 = set(range(1, 26))  # 1-25
        tasks_90_95 = set(range(1, 26)) | {27}  # 1-25, 27
        tasks_95_100 = set(range(1, 28))  # 1-27

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

    # Логика откладывания T26/T27 для первого плана с низким баллом/прогрессом (только для ЕГЭ)
    if student.exam_type == 'ege':
        score_is_high = student.initial_score is not None and student.initial_score >= 60
        tasks_1_to_25 = set(range(1, 26))
        known_tasks_1_to_25 = known_task_numbers.intersection(tasks_1_to_25)
        percentage_known_1_to_25 = (
            (len(known_tasks_1_to_25) / 25) * 100 if tasks_1_to_25 else 0
        )
        core_tasks_learned_enough = percentage_known_1_to_25 >= 50
        should_defer = is_first_plan and not score_is_high and not core_tasks_learned_enough

        if should_defer:
            print("Откладываем T26/T27 для первого плана")
            required_tasks.discard(26)
            required_tasks.discard(27)

    # Квоты T26 и T27 теперь распределяются в предыдущем окне

    # Удаляем уже известные задания
    print(f"Required tasks before known removal: {len(required_tasks)}")

    # Удаляем уже известные задания
    required_tasks.difference_update(known_task_numbers)

    print(
        f"Required tasks after known removal: {len(required_tasks)} -> {sorted(list(required_tasks))}"
    )

    return required_tasks


def _filter_regular_webinars(
    regular_webinars,
    required_tasks,
    known_task_numbers,
    watched_webinar_ids,
    assigned_webinar_ids,
    exam_type='ege',  # Добавляем параметр типа экзамена
):
    """Фильтрует обычные вебинары по релевантности задач и статусу просмотра."""
    available_regular = []
    # Для ОГЭ задания 26 и 27 не существуют
    needs_task_26 = 26 in required_tasks if exam_type == 'ege' else False
    needs_task_27 = 27 in required_tasks if exam_type == 'ege' else False

    print(f"\nФильтрация {len(regular_webinars)} регулярных вебинаров:")
    for w in regular_webinars:
        # ДОБАВЛЕНО: Пропускаем "Нарешку" и "Мини-щелчок", которые не должны автоматически добавляться в план
        if hasattr(w, 'for_mocks') and w.for_mocks:
            print(f"  - Skip {w.id}: Нарешка (for_mocks)")
            continue
        if hasattr(w, 'for_minisnap') and w.for_minisnap:
            print(f"  - Skip {w.id}: Мини-щелчок (for_minisnap)")
            continue
        
        # Дополнительно проверяем название вебинара
        if hasattr(w, 'title') and w.title:
            title_lower = w.title.lower()
            if "нарешка" in title_lower or "наре-шка" in title_lower:
                print(f"  - Skip {w.id}: Нарешка (по названию)")
                continue
            if "мини-щелчок" in title_lower or "мини щелчок" in title_lower:
                print(f"  - Skip {w.id}: Мини-щелчок (по названию)")
                continue
            if "большая нарешка" in title_lower:
                print(f"  - Skip {w.id}: Большая Нарешка (по названию)")
                continue
        
        if w.id in assigned_webinar_ids or w.id in watched_webinar_ids:
            # print(f"  - Skip {w.id}: already assigned or watched")
            continue  # Уже назначен или просмотрен
        if not w.task_numbers:
            # print(f"  - Skip {w.id}: no task numbers")
            continue  # Вебинар без задач

        webinar_tasks = {t.number for t in w.task_numbers}

        # Пропускаем, если все задачи вебинара уже известны
        if known_task_numbers and webinar_tasks.issubset(known_task_numbers):
            # print(f"  - Skip {w.id}: all tasks ({webinar_tasks}) are known")
            continue

        # Пропускаем, если ни одна задача вебинара не пересекается с необходимыми
        has_needed_tasks = webinar_tasks.intersection(required_tasks)

        if not has_needed_tasks:
            # print(f"  - Skip {w.id}: tasks ({webinar_tasks}) do not intersect with required ({required_tasks})")
            continue

        # Дополнительно пропускаем, если вебинар по T26/T27, а они не нужны
        if 26 in webinar_tasks and not needs_task_26:
            # print(f"  - Skip {w.id}: contains T26, but T26 is not needed")
            continue
        if 27 in webinar_tasks and not needs_task_27:
            # print(f"  - Skip {w.id}: contains T27, but T27 is not needed")
            continue

        # print(f"  + Keep {w.id}: relevant tasks found")
        available_regular.append(w)
    print(f"Доступно регулярных вебинаров после фильтрации: {len(available_regular)}")
    return available_regular


# def _group_and_sort_by_task(available_regular, required_tasks):
#     """Группирует вебинары по задачам и сортирует их внутри групп."""
#     webinars_by_task = {task_num: [] for task_num in required_tasks}
#     for webinar in available_regular:
#         webinar_tasks_covered = {t.number for t in webinar.task_numbers}
#         relevant_tasks = webinar_tasks_covered.intersection(required_tasks)
#         for task_num in relevant_tasks:
#             webinars_by_task[task_num].append(webinar)

#     task_deques = {}
#     print("\nГруппировка и сортировка вебинаров по задачам:")
#     for task_num in sorted(list(required_tasks)):
#         webinar_list = webinars_by_task.get(task_num, [])
#         # Убираем дубликаты вебинаров внутри одной задачи (если они как-то попали)
#         unique_webinars = list({w.id: w for w in webinar_list}.values())
#         if unique_webinars:
#             unique_webinars.sort(key=create_webinar_sort_key)
#             task_deques[task_num] = deque(unique_webinars)
#             print(f"  Task {task_num}: {len(task_deques[task_num])} webinars sorted.")
#         else:
#             print(f"  Task {task_num}: No available webinars found.")

#     return task_deques

def _group_and_sort_by_task(available_regular, required_tasks):
   """Группирует вебинары по типам задач и сортирует их внутри групп."""
   
   # Определяем типы задач
   task_types = {
       'regular': set(range(1, 26)),  # Задачи 1-25 для основного курса
       't26': {26},                   # Задача 26
       't27': {27}                    # Задача 27
   }
   
   # Инициализируем группы
   webinars_by_type = {
       'regular': [],
       't26': [],
       't27': []
   }
   
   # Группируем вебинары по типам
   for webinar in available_regular:
       webinar_tasks_covered = {t.number for t in webinar.task_numbers}
       relevant_tasks = webinar_tasks_covered.intersection(required_tasks)
       
       # Определяем к какому типу относится вебинар (с приоритетами)
       if 27 in webinar_tasks_covered and 27 in required_tasks:
           # T27 имеет высший приоритет
           webinars_by_type['t27'].append(webinar)
       elif 26 in webinar_tasks_covered and 26 in required_tasks:
           # T26 имеет следующий приоритет
           webinars_by_type['t26'].append(webinar)
       elif relevant_tasks.intersection(task_types['regular']):
           # Если есть пересечение с обычными задачами
           webinars_by_type['regular'].append(webinar)
   
   # Создаем deque для каждого типа
   task_deques = {}
   print("\nГруппировка и сортировка вебинаров по типам:")
   
   for task_type in ['regular', 't26', 't27']:
       webinar_list = webinars_by_type[task_type]
       
       # Убираем дубликаты вебинаров внутри одного типа
       unique_webinars = list({w.id: w for w in webinar_list}.values())
       
       if unique_webinars:
           unique_webinars.sort(key=create_webinar_sort_key)
           task_deques[task_type] = deque(unique_webinars)
           print(f" {task_type}: {len(task_deques[task_type])} webinars sorted.")
       else:
           print(f" {task_type}: No available webinars found.")
   
   return task_deques


def _distribute_webinars_to_weeks(
    task_deques,
    remaining_beginner_overflow,
    hours_per_week,
    assigned_webinar_ids,  # Модифицируется
    weekly_hours_summary,  # Модифицируется
):
    """
    Распределяет вебинары по неделям с учетом приоритетов.
    Квоты T26 и T27 теперь распределяются в предыдущем окне.
    
    Args:
        task_deques: словарь с очередями вебинаров по типам ('regular', 't26', 't27')
        remaining_beginner_overflow: очередь вебинаров для начинающих, не вошедшие в первую неделю
        hours_per_week: доступные часы в неделю
        assigned_webinar_ids: множество уже назначенных ID вебинаров (модифицируется)
        weekly_hours_summary: словарь часов по неделям (модифицируется)
    
    Returns:
        tuple: (webinar_weeks, selected_regular_webinars)
            webinar_weeks: dict - словарь {id вебинара: номер недели}
            selected_regular_webinars: list - список выбранных вебинаров основного курса
    """
    
    # Словарь для хранения соответствия ID вебинара -> неделя
    webinar_weeks = {}
    selected_regular_webinars = []
    
    # Словарь для хранения часов по неделям (инициализируем из weekly_hours_summary для всех недель)
    weekly_stats = {
        1: {'total': weekly_hours_summary.get(1, 0.0), 't26': 0, 't27': 0, 'regular': 0},
        2: {'total': weekly_hours_summary.get(2, 0.0), 't26': 0, 't27': 0, 'regular': 0},
        3: {'total': weekly_hours_summary.get(3, 0.0), 't26': 0, 't27': 0, 'regular': 0},
        4: {'total': weekly_hours_summary.get(4, 0.0), 't26': 0, 't27': 0, 'regular': 0},
    }
    
    # Счетчики добавленных вебинаров
    total_added = {'t26': 0, 't27': 0, 'regular': 0}
    
    # Квоты T26 и T27 теперь распределяются в предыдущем окне
    print(f"\nРаспределение вебинаров по неделям (часов в неделю: {hours_per_week})")
    
    # Шаг 1: Распределение beginner overflow на вторую неделю
    if remaining_beginner_overflow:
        print("\n--- Распределение beginner overflow (неделя 2) ---")
        while remaining_beginner_overflow:
            w_overflow = remaining_beginner_overflow[0]
            if w_overflow.id in assigned_webinar_ids:
                remaining_beginner_overflow.popleft()
                continue
                
            w_hours = get_webinar_hours(w_overflow)
            
            if weekly_stats[2]['total'] + w_hours <= hours_per_week:
                w_to_add = remaining_beginner_overflow.popleft()
                webinar_weeks[w_to_add.id] = 2  # На вторую неделю
                assigned_webinar_ids.add(w_to_add.id)
                weekly_stats[2]['total'] += w_hours
                weekly_hours_summary[2] = weekly_stats[2]['total']
                print(f"  + Добавлен beginner overflow ID: {w_to_add.id} ({w_hours:.1f}ч). Всего на неделе 2: {weekly_stats[2]['total']:.1f}ч")
            else:
                print(f"  - Пропущен beginner overflow ID: {w_overflow.id} - недостаточно часов")
                break
    
    # Функция для добавления вебинара в план
    def add_webinar_to_plan(webinar, week_number, webinar_type):
        if webinar.id in assigned_webinar_ids:
            return False
        
        webinar_hours = get_webinar_hours(webinar)
        
        # Проверяем, поместится ли вебинар в неделю
        if weekly_stats[week_number]['total'] + webinar_hours <= hours_per_week:
                
            # Добавляем вебинар
            webinar_weeks[webinar.id] = week_number
            if webinar_type != 'beginner':
                selected_regular_webinars.append(webinar)
            assigned_webinar_ids.add(webinar.id)
            
            # Обновляем статистику
            weekly_stats[week_number]['total'] += webinar_hours
            weekly_stats[week_number][webinar_type] += webinar_hours
            weekly_hours_summary[week_number] = weekly_stats[week_number]['total']
            total_added[webinar_type] += 1
            
            print(f"  + Добавлен {webinar_type} ID: {webinar.id} ({webinar_hours:.1f}ч) на неделю {week_number}. " 
                  f"Всего на неделе: {weekly_stats[week_number]['total']:.1f}ч")
            return True
        
        return False
    
    # Шаг 2: Распределение T26/T27 (квоты теперь распределяются в предыдущем окне)
    for task_type in ['t26', 't27']:
        if task_type not in task_deques or not task_deques[task_type]:
            continue
            
        print(f"\n--- Распределение {task_type} вебинаров ---")
            
        # Преобразуем очередь в список, чтобы работать с индексами
        webinar_list = list(task_deques[task_type])
        
        # Вебинары уже отсортированы по create_webinar_sort_key (категория -> дата -> id)
        # Распределяем последовательно по неделям, не перепрыгивая между ними
        current_week = 1  # Начинаем с первой недели
        added_per_week = {1: 0, 2: 0, 3: 0, 4: 0}  # Сколько добавлено в каждую неделю
        
        for webinar in webinar_list:
            # Проверяем, не был ли вебинар уже добавлен
            if webinar.id in assigned_webinar_ids:
                continue
                
            # Пробуем добавить в текущую неделю
            webinar_hours = get_webinar_hours(webinar)
            if weekly_stats[current_week]['total'] + webinar_hours <= hours_per_week:
                # Добавляем вебинар
                webinar_weeks[webinar.id] = current_week
                selected_regular_webinars.append(webinar)
                assigned_webinar_ids.add(webinar.id)
                
                # Обновляем статистику
                weekly_stats[current_week]['total'] += webinar_hours
                weekly_stats[current_week][task_type] += webinar_hours
                weekly_hours_summary[current_week] = weekly_stats[current_week]['total']
                added_per_week[current_week] += 1
                total_added[task_type] += 1
                
                print(f"  + Добавлен {task_type} ID: {webinar.id} ({webinar_hours:.1f}ч) на неделю {current_week}. " 
                      f"Всего на неделе: {weekly_stats[current_week]['total']:.1f}ч")
            else:
                # Не хватает часов в текущей неделе, переходим к следующей
                current_week += 1
                if current_week > 4:
                    # Все недели заполнены
                    break
                # Пробуем добавить в следующую неделю
                if weekly_stats[current_week]['total'] + webinar_hours <= hours_per_week:
                    webinar_weeks[webinar.id] = current_week
                    selected_regular_webinars.append(webinar)
                    assigned_webinar_ids.add(webinar.id)
                    
                    weekly_stats[current_week]['total'] += webinar_hours
                    weekly_stats[current_week][task_type] += webinar_hours
                    weekly_hours_summary[current_week] = weekly_stats[current_week]['total']
                    added_per_week[current_week] += 1
                    total_added[task_type] += 1
                    
                    print(f"  + Добавлен {task_type} ID: {webinar.id} ({webinar_hours:.1f}ч) на неделю {current_week}. " 
                          f"Всего на неделе: {weekly_stats[current_week]['total']:.1f}ч")
                else:
                    print(f"  - Пропущен {task_type} ID: {webinar.id} - не хватает часов")
            
        # Очищаем очередь, так как мы уже обработали все вебинары
        task_deques[task_type].clear()
    
    # Шаг 3: Распределение обычных вебинаров (regular) строго по дате внутри категории
    if 'regular' in task_deques and task_deques['regular']:
        print("\n--- Распределение regular вебинаров ---")
        
        # Преобразуем очередь в список
        regular_webinars = list(task_deques['regular'])
        
        # Группируем вебинары по категории
        webinars_by_category = {}
        for webinar in regular_webinars:
            category = webinar.category if hasattr(webinar, 'category') and webinar.category else 0
            if category not in webinars_by_category:
                webinars_by_category[category] = []
            webinars_by_category[category].append(webinar)
        
        # Приоритет категорий: Обязательные (1) -> Повторение (2) -> Продвинутые (4) -> Необязательные (3) -> Прочие (0)
        category_priority = [1, 2, 4, 3, 0]  # Определяем порядок обработки категорий
        
        # Обрабатываем категории по приоритету
        for category in category_priority:
            if category not in webinars_by_category:
                continue
                
            print(f"  Распределение вебинаров категории {category}")
            
            # Вебинары в категории уже отсортированы по дате
            category_webinars = webinars_by_category[category]
            
            # Заполняем недели последовательно, а не равномерно
            current_week = 1  # Начинаем с первой недели
            for webinar in category_webinars:
                # Проверяем, не был ли вебинар уже добавлен
                if webinar.id in assigned_webinar_ids:
                    continue
                    
                # Пытаемся добавить в текущую неделю
                if current_week <= 4:  # Только если недели 1-4
                    webinar_hours = get_webinar_hours(webinar)
                    if weekly_stats[current_week]['total'] + webinar_hours <= hours_per_week:
                        # Добавляем вебинар в текущую неделю
                        add_webinar_to_plan(webinar, current_week, 'regular')
                    else:
                        # Неделя заполнена, переходим к следующей
                        current_week += 1
                        # Если все недели заполнены, пропускаем вебинар
                        if current_week > 4:
                            print(f"  - Пропущен regular ID: {webinar.id} категории {category} - все недели заполнены")
                            continue
                        # Пробуем добавить в следующую неделю
                        if weekly_stats[current_week]['total'] + webinar_hours <= hours_per_week:
                            add_webinar_to_plan(webinar, current_week, 'regular')
                        else:
                            # Если и в следующую неделю не помещается, пропускаем
                            print(f"  - Пропущен regular ID: {webinar.id} категории {category} - не хватает часов")
                            current_week += 1  # Переходим к следующей неделе для следующих вебинаров
                else:
                    # Если все недели заполнены, пропускаем оставшиеся вебинары
                    print(f"  - Пропущен regular ID: {webinar.id} категории {category} - все недели заполнены")
        
        # Очищаем очередь
        task_deques['regular'].clear()
    
    # Выводим итоговую статистику
    print("\n--- Итоговое распределение вебинаров ---")
    for week in range(1, 5):
        print(f"Неделя {week}: всего {weekly_stats[week]['total']:.1f}ч, " 
              f"T26: {weekly_stats[week]['t26']:.1f}ч, "
              f"T27: {weekly_stats[week]['t27']:.1f}ч, "
              f"regular: {weekly_stats[week]['regular']:.1f}ч")
    
    print(f"Всего добавлено: T26: {total_added['t26']}, T27: {total_added['t27']}, regular: {total_added['regular']}")
    
    return webinar_weeks, selected_regular_webinars


# --- Основная функция (рефакторинг) ---


def recommend_webinars(
    student,
    known_task_numbers,
    watched_webinar_ids,
    is_first_plan=True,
    selected_task_numbers=None,
    include_2025_webinars=False,
    block_quotas=None,
):
    """Подбирает вебинары для плана обучения студента."""
    print("\n=== recommend_webinars START ===")
    print(
        f"Student ID: {student.id}, First Plan: {is_first_plan}, Target: {student.target_score}, Hours: {student.hours_per_week}"
    )
    print(f"Known: {known_task_numbers}, Watched: {watched_webinar_ids}")
    print(f"Block quotas: {block_quotas}")

    # --- 1. Параметры и инициализация ---
    hours_per_week = student.hours_per_week or 9
    webinar_weeks = {}
    weekly_hours_summary = {w: 0.0 for w in range(1, 5)}
    assigned_webinar_ids = set()
    
    # Получение всех вебинаров с фильтрацией по академическому году и типу экзамена
    webinars_query = Webinar.query.options(db.joinedload(Webinar.task_numbers))
    
    # Фильтруем по типу экзамена студента
    webinars_query = webinars_query.filter(Webinar.exam_type == student.exam_type)
    
    # Если не нужно включать вебинары 2025 года, фильтруем их
    if not include_2025_webinars:
        webinars_query = webinars_query.filter(Webinar.academic_year == 2026)
    
    all_webinars = webinars_query.all()
    print(f"Total webinars in DB: {len(all_webinars)}")
    print(f"Academic Year Filter: {'Both 2025 and 2026' if include_2025_webinars else 'Only 2026'}")

    # --- 1.4. Ролики Python с нуля: сначала пытаемся заполнить Неделю 1, остаток в Неделю 2 ---
    selected_beginner_webinars, beginner_weeks, beginner_assigned_ids = _handle_beginner_webinars(
        student,
        all_webinars,
        watched_webinar_ids,
        hours_per_week,
    )
    # Помечаем занятые ID и часы за ролики Python с нуля по неделям
    assigned_webinar_ids.update(beginner_assigned_ids)
    for wid, week in beginner_weeks.items():
        weekly_hours_summary[week] = weekly_hours_summary.get(week, 0.0) + get_webinar_hours(next(w for w in selected_beginner_webinars if w.id == wid))

    # --- 1.5. Анализ блоков вебинаров ---
    # Определяем нужны ли задания 26
    needs_task_26 = False
    if selected_task_numbers:
        needs_task_26 = 26 in selected_task_numbers
    else:
        # Если не переданы выбранные задания, определяем по required_tasks
        required_tasks = _determine_required_tasks(student, known_task_numbers, is_first_plan)
        needs_task_26 = 26 in required_tasks
    
    webinar_blocks = analyze_webinar_blocks(
        all_webinars, 
        watched_webinar_ids, 
        hours_per_week, 
        student.needs_python_basics, 
        is_first_plan, 
        needs_task_26,
        include_2025_webinars
    )
    print(f"Webinar blocks analysis: {[(block, data['count']) for block, data in webinar_blocks.items() if data['count'] > 0]}")
    
    # Применяем недельные квоты блоков если они заданы
    if block_quotas:
        print(f"Applying weekly block quotas: {block_quotas}")
        
        # НОВАЯ ЛОГИКА: Сначала обрабатываем beginner вебинары с правильной сортировкой
        if student.needs_python_basics and 'beginners' in block_quotas and block_quotas['beginners'] > 0:
            print("Processing beginner webinars with correct ordering...")
            beginner_webinars_available = [
                w for w in all_webinars 
                if w.for_beginners and w.id not in watched_webinar_ids
            ]
            beginner_webinars_available.sort(key=_beginner_sort_key)
            
            # Распределяем beginner видео по неделям согласно квоте
            beginner_count = 0
            beginner_webinars_selected = []
            beginner_weeks_mapping = {}
            
            for week in range(1, 5):  # 4 недели
                week_quota = block_quotas['beginners']
                added_this_week = 0
                
                while added_this_week < week_quota and beginner_count < len(beginner_webinars_available):
                    webinar = beginner_webinars_available[beginner_count]
                    beginner_webinars_selected.append(webinar)
                    beginner_weeks_mapping[webinar.id] = week
                    beginner_count += 1
                    added_this_week += 1
                
                # Если beginner ролики закончились, но квота недели не заполнена,
                # запомним это для дозаполнения основным курсом
                if beginner_count >= len(beginner_webinars_available) and added_this_week < week_quota:
                    print(f"Week {week}: beginner videos ended, need {week_quota - added_this_week} more slots to fill with basic course")
                    break
            
            # Подготавливаем модифицированные квоты блоков для остальных вебинаров
            # Если beginner квота не была полностью использована, переносим остаток в basic
            modified_block_quotas = block_quotas.copy()
            total_beginner_needed = block_quotas['beginners'] * 4  # 4 недели
            actual_beginner_count = len(beginner_webinars_selected)
            
            if actual_beginner_count < total_beginner_needed:
                # Beginner ролики закончились, добавляем недостающее количество к basic квоте
                missing_slots = total_beginner_needed - actual_beginner_count
                original_basic_quota = modified_block_quotas.get('basic', 0)
                modified_block_quotas['basic'] = original_basic_quota + (missing_slots // 4)  # Распределяем по неделям
                if missing_slots % 4 > 0:
                    # Если остаток, добавляем еще один в неделю
                    modified_block_quotas['basic'] += 1
                    
                print(f"Beginner videos insufficient: {actual_beginner_count}/{total_beginner_needed}, adding {missing_slots} slots to basic quota")
                print(f"Modified basic quota: {original_basic_quota} -> {modified_block_quotas['basic']}")
            
            # Убираем beginner квоту для остальной обработки
            modified_block_quotas['beginners'] = 0
            
            # Удаляем beginner из общего пула для _filter_webinars_by_block_quotas
            non_beginner_webinars = [w for w in all_webinars if not w.for_beginners]
            
            # Фильтруем остальные вебинары по модифицированным квотам блоков
            other_webinars, other_weeks = _filter_webinars_by_block_quotas(non_beginner_webinars, modified_block_quotas, watched_webinar_ids, hours_per_week)
            
            # Объединяем результаты
            suitable_webinars = beginner_webinars_selected + other_webinars
            webinar_weeks = {**beginner_weeks_mapping, **other_weeks}
            
            print(f"Beginner webinars selected: {len(beginner_webinars_selected)}")
            print(f"Other webinars selected: {len(other_webinars)}")
        else:
            # Обычная логика без beginner обработки
            suitable_webinars, webinar_weeks = _filter_webinars_by_block_quotas(all_webinars, block_quotas, watched_webinar_ids, hours_per_week)
        
        print(f"Webinars after block quotas filtering: {len(suitable_webinars)}")
        
        # Рассчитываем часы по неделям
        for webinar in suitable_webinars:
            week = webinar_weeks[webinar.id]
            webinar_hours = get_webinar_hours(webinar)
            weekly_hours_summary[week] += webinar_hours
        
        print(f"Final weekly hours summary: {weekly_hours_summary}")
        print(f"Final webinar weeks assignment: {webinar_weeks}")
        print("=== recommend_webinars END ===")
        
        return suitable_webinars, webinar_weeks, weekly_hours_summary, webinar_blocks

    # --- 3. Определение необходимых заданий ---
    # Если заданы выбранные задания, используем их вместо определения на основе целевого балла
    if selected_task_numbers:
        required_tasks = set(selected_task_numbers)
        print(f"Используем явно выбранные задания ({len(required_tasks)}): {sorted(list(required_tasks))}")
    else:
        required_tasks = _determine_required_tasks(
            student, known_task_numbers, is_first_plan
        )

    # --- 4. Фильтрация обычных вебинаров ---
    regular_webinars = [w for w in all_webinars if not w.for_beginners]
    
    # Исключаем мини-щелчок для вебинаров 2024-2025 года
    if not include_2025_webinars:
        regular_webinars = [w for w in regular_webinars if not (w.for_minisnap and w.academic_year == 2025)]
    available_regular = _filter_regular_webinars(
        regular_webinars,
        required_tasks,
        known_task_numbers,
        watched_webinar_ids,
        assigned_webinar_ids,
        student.exam_type,  # Передаем тип экзамена
    )

    # --- 5. Проверки на невозможность составить план ---
    if not required_tasks and not student.needs_python_basics:
        print(
            "Нет необходимых заданий для изучения и Python не нужен, план не может быть составлен."
        )
        return [], {}, {}
    if (
        not available_regular
        and not selected_beginner_webinars
        and not remaining_beginner_overflow
    ):
        # Дополнительно проверяем, остались ли required_tasks. Если да, значит просто нет вебов.
        if required_tasks:
            print("Нет доступных вебинаров для необходимых заданий.")
        else:
            print(
                "Все необходимые задания изучены, и нет доступных вебинаров для повторения или других категорий."
            )
        return [], {}, {}

    # --- 6. Группировка и сортировка по задачам ---
    task_deques = _group_and_sort_by_task(available_regular, required_tasks)

    # --- 7. Распределение по неделям ---
    final_webinar_weeks, selected_regular_webinars = _distribute_webinars_to_weeks(
        task_deques,
        deque(),
        hours_per_week,
        assigned_webinar_ids,  # Модифицируется
        weekly_hours_summary,  # Модифицируется
    )
    # Добавляем недели для beginner вебинаров к итоговому словарю
    final_webinar_weeks.update({w.id: beginner_weeks[w.id] for w in selected_beginner_webinars})

    # --- 8. Сборка результатов ---
    all_selected_webinars = selected_beginner_webinars + selected_regular_webinars

    # Финальная проверка на дубликаты (на всякий случай)
    final_selected_ids = [w.id for w in all_selected_webinars]
    if len(final_selected_ids) != len(set(final_selected_ids)):
        print("!!! WARNING: Duplicate IDs found in recommend_webinars final output!")
        id_counts = Counter(final_selected_ids)
        duplicates = {id: count for id, count in id_counts.items() if count > 1}
        print(f"Duplicate IDs and counts: {duplicates}")

    # --- 9. Возврат результата и финальная отладка ---
    print(f"Total webinars selected: {len(all_selected_webinars)}")
    print(f"Final weekly hours summary: {weekly_hours_summary}")
    print(f"Final webinar weeks assignment: {final_webinar_weeks}")
    print("=== recommend_webinars END ===\n")
    return all_selected_webinars, final_webinar_weeks, weekly_hours_summary, webinar_blocks
