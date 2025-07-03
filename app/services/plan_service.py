from datetime import datetime, date
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


def _handle_beginner_webinars(
    student, all_webinars, watched_webinar_ids, hours_per_week
):
    """Обрабатывает вебинары 'Python с нуля'."""
    selected_beginner_webinars = []
    remaining_beginner_overflow = deque()
    beginner_assigned_ids = set()
    week1_hours = 0.0

    if student.needs_python_basics:
        beginner_webinars_available = [
            w
            for w in all_webinars
            if w.for_beginners and w.id not in watched_webinar_ids
        ]
        print(
            f"\nНайдено доступных beginner вебинаров: {len(beginner_webinars_available)}"
        )
        for w in beginner_webinars_available:
            w_hours = get_webinar_hours(w)
            if week1_hours + w_hours <= hours_per_week:
                selected_beginner_webinars.append(w)
                beginner_assigned_ids.add(w.id)
                week1_hours += w_hours
            else:
                remaining_beginner_overflow.append(w)
        print(
            f"Добавлено beginner (Неделя 1): {len(selected_beginner_webinars)} вебинаров ({week1_hours} часов)"
        )
        print(
            f"Осталось beginner для Недели 2: {len(remaining_beginner_overflow)} вебинаров"
        )
    else:
        print("\nPython Basics не требуется.")

    return (
        selected_beginner_webinars,
        remaining_beginner_overflow,
        beginner_assigned_ids,
        week1_hours,
    )


def _determine_required_tasks(
    student, known_task_numbers, is_first_plan, quota_t26=0, quota_t27=0
):
    """Определяет необходимые задания с учетом балла, известных и логики откладывания."""
    required_tasks = set()
    # Определяем базовый набор заданий по целевому баллу
    target_score = (
        student.target_score or 85
    )  # Используем 85 как дефолт, если не указано
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

    # Логика откладывания T26/T27 для первого плана с низким баллом/прогрессом
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

    # --- ДОБАВЛЕНО: Принудительное включение T26/T27 при установленных квотах ---
    if quota_t26 > 0 and not should_defer:
        required_tasks.add(26)
        print(
            f"Задание 26 добавлено в required_tasks из-за установленной квоты ({quota_t26})"
        )

    if quota_t27 > 0 and not should_defer:
        required_tasks.add(27)
        print(
            f"Задание 27 добавлено в required_tasks из-за установленной квоты ({quota_t27})"
        )
    # --- КОНЕЦ ДОБАВЛЕННОГО КОДА ---

    # Удаляем уже известные задания
    print(f"Required tasks before known removal: {len(required_tasks)}")

    # --- МОДИФИЦИРОВАНО: Не удаляем T26/T27 при установленных квотах ---
    if quota_t26 > 0 and 26 in known_task_numbers:
        known_task_numbers_copy = known_task_numbers.copy()
        known_task_numbers_copy.discard(26)
        print(f"Задание 26 не будет исключено из-за установленной квоты ({quota_t26})")
    else:
        known_task_numbers_copy = known_task_numbers

    if quota_t27 > 0 and 27 in known_task_numbers_copy:
        known_task_numbers_copy = known_task_numbers_copy.copy()
        known_task_numbers_copy.discard(27)
        print(f"Задание 27 не будет исключено из-за установленной квоты ({quota_t27})")

    required_tasks.difference_update(known_task_numbers_copy)
    # --- КОНЕЦ МОДИФИКАЦИИ ---

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
    quota_t26=0,
    quota_t27=0,
):
    """Фильтрует обычные вебинары по релевантности задач и статусу просмотра."""
    available_regular = []
    needs_task_26 = (
        26 in required_tasks or quota_t26 > 0
    )  # МОДИФИЦИРОВАНО: учитываем квоту
    needs_task_27 = (
        27 in required_tasks or quota_t27 > 0
    )  # МОДИФИЦИРОВАНО: учитываем квоту

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
            # МОДИФИЦИРОВАНО: Не пропускаем T26/T27 вебинары при установленных квотах
            has_t26 = 26 in webinar_tasks and quota_t26 > 0
            has_t27 = 27 in webinar_tasks and quota_t27 > 0
            if has_t26 or has_t27:
                pass  # Не пропускаем вебинары с T26/T27 если установлены квоты
            else:
                # print(f"  - Skip {w.id}: all tasks ({webinar_tasks}) are known")
                continue

        # Пропускаем, если ни одна задача вебинара не пересекается с необходимыми
        has_needed_tasks = webinar_tasks.intersection(required_tasks)
        # МОДИФИЦИРОВАНО: Дополнительно проверяем на T26/T27 при установленных квотах
        has_t26_with_quota = 26 in webinar_tasks and quota_t26 > 0
        has_t27_with_quota = 27 in webinar_tasks and quota_t27 > 0

        if not has_needed_tasks and not has_t26_with_quota and not has_t27_with_quota:
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
    quota_t26,
    quota_t27,
    assigned_webinar_ids,  # Модифицируется
    weekly_hours_summary,  # Модифицируется
):
    """
    Распределяет вебинары по неделям с учетом квот и приоритетов.
    
    Args:
        task_deques: словарь с очередями вебинаров по типам ('regular', 't26', 't27')
        remaining_beginner_overflow: очередь вебинаров для начинающих, не вошедшие в первую неделю
        hours_per_week: доступные часы в неделю
        quota_t26: квота вебинаров для задания 26 (количество вебинаров)
        quota_t27: квота вебинаров для задания 27 (количество вебинаров)
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
    
    # Словарь для хранения часов по неделям
    weekly_stats = {
        1: {'total': weekly_hours_summary[1], 't26': 0, 't27': 0, 'regular': 0},
        2: {'total': 0, 't26': 0, 't27': 0, 'regular': 0},
        3: {'total': 0, 't26': 0, 't27': 0, 'regular': 0},
        4: {'total': 0, 't26': 0, 't27': 0, 'regular': 0},
    }
    
    # Счетчики добавленных вебинаров
    total_added = {'t26': 0, 't27': 0, 'regular': 0}
    
    # Расчет квот по часам для каждого типа вебинаров
    max_t26_hours = hours_per_week * 0.35 if quota_t26 > 0 else 0  # 35% на T26
    max_t27_hours = hours_per_week * 0.35 if quota_t27 > 0 else 0  # 35% на T27
    
    print(f"\nРасчет квот: T26 = {max_t26_hours:.1f}ч, T27 = {max_t27_hours:.1f}ч из {hours_per_week}ч")
    
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
            # Для T26/T27 проверяем квоты
            if webinar_type == 't26':
                max_hours = hours_per_week * 0.35  # 35% от недельного времени
                if weekly_stats[week_number]['t26'] + webinar_hours > max_hours:
                    return False
            elif webinar_type == 't27':
                max_hours = hours_per_week * 0.35  # 35% от недельного времени
                if weekly_stats[week_number]['t27'] + webinar_hours > max_hours:
                    return False
                
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
    
    # Шаг 2: Распределение T26/T27
    for task_type in ['t26', 't27']:
        if task_type not in task_deques or not task_deques[task_type]:
            continue
            
        print(f"\n--- Распределение {task_type} вебинаров ---")
        quota = quota_t26 if task_type == 't26' else quota_t27
        if quota <= 0:
            continue
            
        # Преобразуем очередь в список, чтобы работать с индексами
        webinar_list = list(task_deques[task_type])
        
        # Вебинары уже отсортированы по create_webinar_sort_key (категория -> дата -> id)
        # Распределяем последовательно по неделям, не перепрыгивая между ними
        current_week = 1  # Начинаем с первой недели
        added_per_week = {1: 0, 2: 0, 3: 0, 4: 0}  # Сколько добавлено в каждую неделю
        
        for webinar in webinar_list:
            # Если в текущей неделе достигнута квота или добавлено максимальное количество
            if added_per_week[current_week] >= quota:
                # Переходим к следующей неделе
                current_week += 1
                if current_week > 4:
                    # Все недели заполнены до квоты
                    break
            
            # Проверяем, не был ли вебинар уже добавлен
            if webinar.id in assigned_webinar_ids:
                continue
                
            # Пробуем добавить в текущую неделю
            webinar_hours = get_webinar_hours(webinar)
            if weekly_stats[current_week]['total'] + webinar_hours <= hours_per_week:
                # Проверяем квоту по часам (35% от недельных часов)
                max_hours = hours_per_week * 0.35
                type_hours = weekly_stats[current_week][task_type]
                
                if type_hours + webinar_hours <= max_hours:
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
                # Не хватает часов в текущей неделе
                print(f"  - Пропущен {task_type} ID: {webinar.id} - не хватает часов в неделе {current_week}")
                # НЕ переходим к следующей неделе здесь
            
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
    quota_t26=0,
    quota_t27=0,
    selected_task_numbers=None,
    include_2025_webinars=False,
):
    """Подбирает вебинары для плана обучения студента."""
    print("\n=== recommend_webinars START ===")
    print(
        f"Student ID: {student.id}, First Plan: {is_first_plan}, Target: {student.target_score}, Hours: {student.hours_per_week}"
    )
    print(f"Known: {known_task_numbers}, Watched: {watched_webinar_ids}")
    print(f"Quotas: T26={quota_t26}, T27={quota_t27}")

    # --- 1. Параметры и инициализация ---
    hours_per_week = student.hours_per_week or 9
    webinar_weeks = {}
    weekly_hours_summary = {w: 0.0 for w in range(1, 5)}
    assigned_webinar_ids = set()
    
    # Получение всех вебинаров с фильтрацией по академическому году
    webinars_query = Webinar.query.options(db.joinedload(Webinar.task_numbers))
    
    # Если не нужно включать вебинары 2025 года, фильтруем их
    if not include_2025_webinars and hasattr(Webinar, 'academic_year'):
        webinars_query = webinars_query.filter(Webinar.academic_year == 2026)
    
    all_webinars = webinars_query.all()
    print(f"Total webinars in DB: {len(all_webinars)}")
    print(f"Academic Year Filter: {'Both 2025 and 2026' if include_2025_webinars else 'Only 2026'}")

    # --- 2. Обработка вебинаров "Python с нуля" ---
    (
        selected_beginner_webinars,
        remaining_beginner_overflow,
        beginner_assigned_ids,
        week1_hours,
    ) = _handle_beginner_webinars(
        student, all_webinars, watched_webinar_ids, hours_per_week
    )

    assigned_webinar_ids.update(beginner_assigned_ids)
    # Назначаем недели для beginner вебинаров сразу
    for w in selected_beginner_webinars:
        webinar_weeks[w.id] = 1
    weekly_hours_summary[1] = week1_hours

    # --- 3. Определение необходимых заданий ---
    # Если заданы выбранные задания, используем их вместо определения на основе целевого балла
    if selected_task_numbers:
        required_tasks = set(selected_task_numbers)
        print(f"Используем явно выбранные задания ({len(required_tasks)}): {sorted(list(required_tasks))}")
    else:
        required_tasks = _determine_required_tasks(
            student, known_task_numbers, is_first_plan, quota_t26, quota_t27
        )

    # --- 4. Фильтрация обычных вебинаров ---
    regular_webinars = [w for w in all_webinars if not w.for_beginners]
    available_regular = _filter_regular_webinars(
        regular_webinars,
        required_tasks,
        known_task_numbers,
        watched_webinar_ids,
        assigned_webinar_ids,
        quota_t26,
        quota_t27,
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
        remaining_beginner_overflow,
        hours_per_week,
        quota_t26,
        quota_t27,
        assigned_webinar_ids,  # Модифицируется
        weekly_hours_summary,  # Модифицируется
    )
    # Добавляем недели для beginner вебинаров к итоговому словарю
    final_webinar_weeks.update({w.id: 1 for w in selected_beginner_webinars})

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
    return all_selected_webinars, final_webinar_weeks, weekly_hours_summary
