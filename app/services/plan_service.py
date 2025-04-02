from datetime import datetime
from app.models import Webinar, WatchedWebinar, KnownTaskNumber
import math
from datetime import datetime, date


def recommend_webinars(student, webinars, known_task_numbers, watched_webinar_ids, 
                         is_first_plan=True, last_plan_completion_perc=0.0):
    """Подбирает подходящие вебинары (v3.4 - учет первого плана и выполнения >60%)."""

    print("\n=== Отладка recommend_webinars v3.4 ===")
    print(f"Student ID: {student.id}")
    print(f"Task 26 deferred (start): {student.task_26_deferred}")
    print(f"Task 27 deferred (start): {student.task_27_deferred}")
    print(f"Needs Python Basics: {student.needs_python_basics}")
    print(f"Initial score: {student.initial_score}")
    print(f"Target score: {student.target_score}")
    print(f"Hours per week: {student.hours_per_week}")
    print(f"Is First Plan: {is_first_plan}")
    print(f"Last Plan Completion: {last_plan_completion_perc*100:.1f}%")
    print(f"Known tasks: {known_task_numbers}")
    print(f"Watched webinars: {len(watched_webinar_ids)}")


    # --- 1. Расчет базовых параметров ---
    hours_per_week = student.hours_per_week or 9 # Часов в неделю (минимум 9 по умолчанию)
    avg_hours_per_webinar = 3 # Среднее время на вебинар
    max_webinars_per_week = math.floor(hours_per_week / avg_hours_per_webinar) # Максимум вебинаров в неделю (округление вниз)
    if max_webinars_per_week == 0: max_webinars_per_week = 1 # Минимум 1 вебинар в неделю
    initial_total_webinars_in_plan = max_webinars_per_week * 5 # Изначальное общее кол-во вебинаров

    print("\nРасчет базовых параметров:")
    print(f"Hours per week: {hours_per_week}")
    print(f"Max webinars per week: {max_webinars_per_week}")
    print(f"Total webinars in plan (target): {initial_total_webinars_in_plan}")

    webinar_weeks = {} # Словарь для хранения недели каждого вебинара {webinar_id: week_num}
    selected_beginner_webinars = []
    remaining_webinars = list(webinars) # Копируем список для модификации

    # --- 2. Обработка "Python с нуля" ---
    num_beginner_added = 0
    if student.needs_python_basics:
        beginner_webinars_available = [w for w in remaining_webinars if w.for_beginners and w.id not in watched_webinar_ids]
        print(f"\nНайдено доступных beginner вебинаров: {len(beginner_webinars_available)}")
        # Добавляем beginner вебинары, но не больше, чем общее кол-во в плане
        num_beginner_to_add = min(len(beginner_webinars_available), initial_total_webinars_in_plan)
        for i, w in enumerate(beginner_webinars_available):
            if i >= num_beginner_to_add: break
            webinar_weeks[w.id] = 1 # Всегда в 1 неделю
            selected_beginner_webinars.append(w)
            num_beginner_added += 1
        print(f"Добавлено beginner: {num_beginner_added}")
        # Удаляем beginner вебинары из дальнейшего рассмотрения
        remaining_webinars = [w for w in remaining_webinars if not w.for_beginners]
    else:
        print("\nPython Basics не требуется.")

    # Кол-во слотов, оставшееся для обычных вебинаров
    total_slots_for_regular = initial_total_webinars_in_plan - num_beginner_added
    if total_slots_for_regular < 0: total_slots_for_regular = 0
    print(f"Слотов для обычных вебинаров: {total_slots_for_regular}")


    # --- 3. Определение необходимых заданий и ОБРАБОТКА ОТЛОЖЕННЫХ ---
    required_tasks = set()
    needs_task_26 = False # Нужен ли 26 в ЭТОМ плане
    needs_task_27 = False # Нужен ли 27 в ЭТОМ плане
    was_task_26_deferred = student.task_26_deferred # Был ли 26 отложен с ПРОШЛОГО плана
    was_task_27_deferred = student.task_27_deferred # Был ли 27 отложен с ПРОШЛОГО плана

    # Определяем required_tasks СТРОГО по таблице
    tasks_60_70 = {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 22}
    tasks_70_80 = set(range(1, 13)) | {14} | set(range(16, 24)) # 1-12, 14, 16-23
    tasks_80_85 = set(range(1, 24)) | {25} # 1-23, 25
    tasks_85_90 = set(range(1, 26)) # 1-25
    tasks_90_95 = set(range(1, 26)) | {27} # 1-25, 27
    tasks_95_100 = set(range(1, 28)) # 1-27

    if student.target_score:
        score = student.target_score
        if score <= 70: required_tasks = tasks_60_70.copy()
        elif score <= 80: required_tasks = tasks_70_80.copy()
        elif score <= 85: required_tasks = tasks_80_85.copy()
        elif score <= 90: required_tasks = tasks_85_90.copy()
        elif score <= 95: required_tasks = tasks_90_95.copy()
        else: required_tasks = tasks_95_100.copy()

        # Определяем needs_task_26/27 на основе ИЗНАЧАЛЬНОГО required_tasks по score
        needs_task_26_initial = 26 in required_tasks
        needs_task_27_initial = 27 in required_tasks

        print(f"\nОпределение необходимых заданий (по score={student.target_score}):")
        print(f"Required tasks (initial): {sorted(list(required_tasks))}")
        print(f"Needs task 26 (initial): {needs_task_26_initial}")
        print(f"Needs task 27 (initial): {needs_task_27_initial}")

        # Финальные needs_task для ЭТОГО плана по умолчанию равны initial
        needs_task_26 = needs_task_26_initial
        needs_task_27 = needs_task_27_initial

        # Обрабатываем ОТЛОЖЕННЫЕ задания: включаем их в план, если они были deferred
        if was_task_27_deferred:
            needs_task_27 = True # Убеждаемся, что 27 точно нужно в этом плане
            required_tasks.add(27) # Добавляем в required_tasks
            print(f"Задание 27 БЫЛО отложено, будет включено в план.")
            student.task_27_deferred = False # Сбрасываем флаг
            print("Флаг task_27_deferred сброшен")

        if was_task_26_deferred:
            needs_task_26 = True # Убеждаемся, что 26 точно нужно в этом плане
            required_tasks.add(26) # Добавляем в required_tasks
            print(f"Задание 26 БЫЛО отложено, будет включено в план.")
            student.task_26_deferred = False # Сбрасываем флаг
            print("Флаг task_26_deferred сброшен")

        # --- НОВАЯ ЛОГИКА: Откладываем 26/27 на БУДУЩЕЕ? ---
        # Условие для откладывания: (Низкий балл ИЛИ балла нет) И (Это первый план ИЛИ прошлый < 60%)
        should_defer_due_to_score_and_history = \
            (student.initial_score is None or student.initial_score <= 40) and \
            (is_first_plan or last_plan_completion_perc < 0.60)

        if should_defer_due_to_score_and_history:
            print("\nУсловие для откладывания 26/27 выполнено (score/history).")
            # Откладываем, только если задание изначально было нужно И оно не было обработано как deferred выше
            if needs_task_26_initial and not was_task_26_deferred:
                needs_task_26 = False # Убираем из текущего
                required_tasks.discard(26)
                student.task_26_deferred = True # Ставим флаг для будущего
                print("Откладываем Task 26 на след. план.")
            if needs_task_27_initial and not was_task_27_deferred:
                needs_task_27 = False # Убираем из текущего
                required_tasks.discard(27)
                student.task_27_deferred = True # Ставим флаг для будущего
                print("Откладываем Task 27 на след. план.")
    else:
         # Если target_score не задан, считаем, что все базовые нужны (кроме 26/27)
         required_tasks = tasks_85_90.copy() # Берем как основу 1-25
         needs_task_26 = False
         needs_task_27 = False
         # Но если были отложены - добавляем
         if was_task_27_deferred:
             needs_task_27 = True; required_tasks.add(27); student.task_27_deferred = False
             print("Задание 27 БЫЛО отложено (без target_score), будет включено. Флаг сброшен.")
         if was_task_26_deferred:
             needs_task_26 = True; required_tasks.add(26); student.task_26_deferred = False
             print("Задание 26 БЫЛО отложено (без target_score), будет включено. Флаг сброшен.")

    # Удаляем уже известные задания из required_tasks
    if known_task_numbers:
        print(f"Удаление известных заданий {known_task_numbers} из required_tasks.")
        required_tasks.difference_update(known_task_numbers)
        # Если после удаления известных не осталось нужных 26/27, сбрасываем флаги
        if needs_task_26 and 26 not in required_tasks: needs_task_26 = False
        if needs_task_27 and 27 not in required_tasks: needs_task_27 = False


    print(f"\nИтоговые параметры для плана:")
    print(f"Required tasks (final): {sorted(list(required_tasks))}")
    print(f"Needs task 26 (current plan): {needs_task_26}")
    print(f"Needs task 27 (current plan): {needs_task_27}")
    print(f"Task 26 deferred (for next plan): {student.task_26_deferred}")
    print(f"Task 27 deferred (for next plan): {student.task_27_deferred}")


    # --- 4. Фильтрация оставшихся вебинаров ---
    filtered_webinars = []
    print(f"\nФильтрация вебинаров (проверка по required_tasks: {sorted(list(required_tasks))} ):")
    for w in remaining_webinars:
        # Пропускаем просмотренные
        if w.id in watched_webinar_ids: continue

        # НОВЫЙ ФИЛЬТР: Пропускаем 'Python для начинающих', если он не нужен
        if not student.needs_python_basics and w.title and "python для начинающих" in w.title.lower():
            print(f"  - Skip (Beginner title excluded): {w.title[:60]}...")
            continue

        # Пропускаем, если нет номеров заданий
        if not w.task_numbers: continue

        webinar_tasks = {t.number for t in w.task_numbers}

        # Пропускаем, если все задания вебинара уже известны
        if known_task_numbers and webinar_tasks.issubset(known_task_numbers): continue

        # Пропускаем, если НИ ОДНО задание вебинара не входит в required_tasks
        if not webinar_tasks.intersection(required_tasks): continue

        # Пропускаем вебинары 26/27, если они НЕ нужны в этом плане
        if 26 in webinar_tasks and not needs_task_26: continue
        if 27 in webinar_tasks and not needs_task_27: continue

        filtered_webinars.append(w)

    print(f"Всего вебинаров после фильтрации: {len(filtered_webinars)}")


    # --- 5. Категоризация и сортировка вебинаров ---
    basic_webinars = []
    task26_webinars = []
    task27_webinars = []

    for webinar in filtered_webinars:
        task_nums = {task.number for task in webinar.task_numbers}
        is_task_26 = 26 in task_nums
        is_task_27 = 27 in task_nums

        # Распределяем по категориям, только если задание НУЖНО в этом плане
        if is_task_27 and needs_task_27:
            task27_webinars.append(webinar)
        elif is_task_26 and needs_task_26: # elif, т.к. вебинар может быть и на 26, и на 27
            task26_webinars.append(webinar)
        else:
            # Все остальное идет в базовые (задания 1-25 или ниже)
            basic_webinars.append(webinar)

    print(f"\nКатегоризация вебинаров:")
    print(f"Task 27 webinars: {len(task27_webinars)}")
    print(f"Task 26 webinars: {len(task26_webinars)}")
    print(f"Basic webinars: {len(basic_webinars)}")

    # --- 5.5 Улучшенная сортировка вебинаров ---
    def get_sortable_datetime_with_nulls_last(webinar_date):
        if webinar_date:
            dt_obj = None
            if isinstance(webinar_date, datetime): dt_obj = webinar_date
            elif isinstance(webinar_date, date): dt_obj = datetime.combine(webinar_date, datetime.min.time())
            if dt_obj:
                 # Учитываем timezone, если она есть, иначе считаем naive
                 aware_dt = dt_obj.replace(tzinfo=None) if dt_obj.tzinfo else dt_obj
                 return (0, aware_dt) # (0, date) - приоритет для дат
        return (1, datetime(2000, 1, 1)) # (1, ...) - без даты идут позже

    def sort_key_basic(webinar):
        # Просто по дате, nulls last
        date_key = get_sortable_datetime_with_nulls_last(webinar.date)
        return (date_key[0], date_key[1]) # (0/1, date)

    def sort_key_task27(webinar):
        # Приоритет кластерам, затем дата (nulls last)
        is_cluster = "кластер" in webinar.title.lower() if webinar.title else False
        primary_key = 0 if is_cluster else 1 # Кластеры первее
        date_key = get_sortable_datetime_with_nulls_last(webinar.date)
        return (primary_key, date_key[0], date_key[1]) # (0/1, 0/1, date)

    basic_webinars.sort(key=sort_key_basic)
    task26_webinars.sort(key=sort_key_basic)
    task27_webinars.sort(key=sort_key_task27)

    print("Сортировка вебинаров завершена.")
    # print("Top 3 Task 27:", [(w.title, w.date) for w in task27_webinars[:3]])
    # print("Top 3 Task 26:", [(w.title, w.date) for w in task26_webinars[:3]])
    # print("Top 3 Basic:", [(w.title, w.date) for w in basic_webinars[:3]])


    # --- 6. Расчет целевого кол-ва и распределение по неделям (v3.3 - стандартное округление, приоритет недельной квоте) ---

    # Определяем проценты (логика остается прежней)
    perc_t26, perc_t27, perc_basic = 0.0, 0.0, 1.0
    if was_task_26_deferred and was_task_27_deferred: perc_t26, perc_t27, perc_basic = 0.30, 0.30, 0.40
    elif was_task_27_deferred: perc_t27, perc_t26, perc_basic = 0.40, 0.0, 0.60
    elif was_task_26_deferred: perc_t26, perc_t27, perc_basic = 0.30, 0.0, 0.70
    elif needs_task_26 and needs_task_27: perc_t26, perc_t27, perc_basic = 0.25, 0.25, 0.50
    elif needs_task_27: perc_t27, perc_t26, perc_basic = 0.34, 0.0, 0.66
    elif needs_task_26: perc_t26, perc_t27, perc_basic = 0.34, 0.0, 0.66
    if not needs_task_26: perc_basic += perc_t26; perc_t26 = 0.0
    if not needs_task_27: perc_basic += perc_t27; perc_t27 = 0.0
    perc_basic = min(1.0, max(0.0, perc_basic))

    # Считаем ГЛОБАЛЬНЫЕ цели, используя round()
    target_t27 = round(total_slots_for_regular * perc_t27)
    target_t26 = round(total_slots_for_regular * perc_t26)
    target_sum_advanced = target_t26 + target_t27
    target_basic = total_slots_for_regular - target_sum_advanced
    # Коррекция базовых, если сумма не сходится
    current_sum = target_t26 + target_t27 + target_basic
    diff = total_slots_for_regular - current_sum
    if diff != 0: target_basic += diff
    target_t27 = max(0, target_t27); target_t26 = max(0, target_t26); target_basic = max(0, target_basic)
    if target_basic < 0: # Финальная коррекция, если basic ушел в минус
        deficit = abs(target_basic); can_reduce_t26 = min(deficit, target_t26); target_t26 -= can_reduce_t26; deficit -= can_reduce_t26; can_reduce_t27 = min(deficit, target_t27); target_t27 -= can_reduce_t27; target_basic = 0

    print(f"\nРасчет ГЛОБАЛЬНЫХ целей (из {total_slots_for_regular} слотов, round()):")
    print(f"  Target T27: {target_t27} ({perc_t27*100:.1f}%)")
    print(f"  Target T26: {target_t26} ({perc_t26*100:.1f}%)")
    print(f"  Target Basic: {target_basic} ({perc_basic*100:.1f}%)")
    print(f"  Target Sum: {target_t26 + target_t27 + target_basic} == {total_slots_for_regular}?")

    # --- Понедельное распределение ---
    selected_regular_webinars = []
    assigned_webinar_ids = set(w.id for w in selected_beginner_webinars)
    available_t27 = task27_webinars[:]; available_t26 = task26_webinars[:]; available_basic = basic_webinars[:]
    global_count_t27_added = 0; global_count_t26_added = 0; global_count_basic_added = 0

    print("\n--- Начало понедельного распределения (v3.3) ---")
    for week_num in range(1, 6):
        # НОВОЕ: Пропускаем заполнение Недели 1 обычными вебинарами, если есть Python Basics
        if student.needs_python_basics and week_num == 1:
            print(f"--- Неделя 1 (Заполнена Python Basics) ---")
            # Убедимся, что для вебинаров Python Basics неделя установлена в 1
            for b_webinar in selected_beginner_webinars:
                if b_webinar.id not in webinar_weeks:
                     webinar_weeks[b_webinar.id] = 1
            continue # Переходим к следующей неделе

        # Рассчитываем ЕЖЕНЕДЕЛЬНЫЕ квоты, используя round()
        weekly_quota_t27 = round(max_webinars_per_week * perc_t27)
        weekly_quota_t26 = round(max_webinars_per_week * perc_t26)
        # Базовые получают остаток
        weekly_sum_advanced = weekly_quota_t27 + weekly_quota_t26
        weekly_quota_basic = max_webinars_per_week - weekly_sum_advanced
        # Коррекция, если сумма не сходится
        current_weekly_sum = weekly_quota_t27 + weekly_quota_t26 + weekly_quota_basic
        weekly_diff = max_webinars_per_week - current_weekly_sum
        if weekly_diff != 0: weekly_quota_basic += weekly_diff
        # Финальная проверка на >= 0
        weekly_quota_t27 = max(0, weekly_quota_t27); weekly_quota_t26 = max(0, weekly_quota_t26); weekly_quota_basic = max(0, weekly_quota_basic)
        if weekly_quota_basic < 0: # Маловероятно, но все же
             deficit = abs(weekly_quota_basic); r_t26 = min(deficit, weekly_quota_t26); weekly_quota_t26 -= r_t26; deficit -= r_t26; r_t27 = min(deficit, weekly_quota_t27); weekly_quota_t27 -= r_t27; weekly_quota_basic = 0


        slots_filled_this_week = 0
        weekly_count_t27 = 0; weekly_count_t26 = 0; weekly_count_basic = 0
        print(f"--- Неделя {week_num} (Макс: {max_webinars_per_week}) ---")
        print(f"  Weekly Quotas (round()): T27={weekly_quota_t27}, T26={weekly_quota_t26}, Basic={weekly_quota_basic}")

        def get_next_valid_webinar(webinar_list):
             while webinar_list:
                webinar = webinar_list[0]
                if webinar.id not in assigned_webinar_ids:
                    return webinar_list.pop(0)
                else:
                    webinar_list.pop(0)
             return None

        # Этап 1: Заполняем неделю, ПРИОРИТЕТНО соблюдая НЕДЕЛЬНЫЕ квоты
        # print("  Этап 1: Заполнение по квотам (без проверки глобальных целей)...")
        while slots_filled_this_week < max_webinars_per_week:
            added_in_pass_quota = False

            # 1. Пытаемся добавить Task 27 (в рамках НЕДЕЛЬНОЙ квоты)
            if weekly_count_t27 < weekly_quota_t27 and slots_filled_this_week < max_webinars_per_week:
                webinar = get_next_valid_webinar(available_t27)
                if webinar:
                    webinar_weeks[webinar.id] = week_num; selected_regular_webinars.append(webinar); assigned_webinar_ids.add(webinar.id)
                    global_count_t27_added += 1; weekly_count_t27 += 1; slots_filled_this_week += 1; added_in_pass_quota = True
                    print(f"  +Q T27 (W:{weekly_count_t27}/{weekly_quota_t27}): {webinar.title[:40]}...")

            # 2. Пытаемся добавить Task 26 (в рамках НЕДЕЛЬНОЙ квоты)
            if weekly_count_t26 < weekly_quota_t26 and slots_filled_this_week < max_webinars_per_week:
                webinar = get_next_valid_webinar(available_t26)
                if webinar:
                    webinar_weeks[webinar.id] = week_num; selected_regular_webinars.append(webinar); assigned_webinar_ids.add(webinar.id)
                    global_count_t26_added += 1; weekly_count_t26 += 1; slots_filled_this_week += 1; added_in_pass_quota = True
                    print(f"  +Q T26 (W:{weekly_count_t26}/{weekly_quota_t26}): {webinar.title[:40]}...")

            # 3. Пытаемся добавить Basic (в рамках НЕДЕЛЬНОЙ квоты)
            if weekly_count_basic < weekly_quota_basic and slots_filled_this_week < max_webinars_per_week:
                webinar = get_next_valid_webinar(available_basic)
                if webinar:
                    webinar_weeks[webinar.id] = week_num; selected_regular_webinars.append(webinar); assigned_webinar_ids.add(webinar.id)
                    global_count_basic_added += 1; weekly_count_basic += 1; slots_filled_this_week += 1; added_in_pass_quota = True
                    print(f"  +Q Bas (W:{weekly_count_basic}/{weekly_quota_basic}): {webinar.title[:40]}...")

            # Если не смогли ничего добавить по квотам
            if not added_in_pass_quota:
                break # Выходим из цикла заполнения по квотам

        # Этап 2: Дозаполнение недели, если остались места (с проверкой ГЛОБАЛЬНЫХ целей)
        if slots_filled_this_week < max_webinars_per_week:
            # print("  Этап 2: Дозаполнение (с проверкой глобальных целей)...")
            while slots_filled_this_week < max_webinars_per_week:
                added_in_fill = False
                # Пытаемся добрать T27 (если ГЛОБАЛЬНАЯ цель не достигнута)
                if global_count_t27_added < target_t27:
                    webinar = get_next_valid_webinar(available_t27)
                    if webinar:
                        webinar_weeks[webinar.id] = week_num; selected_regular_webinars.append(webinar); assigned_webinar_ids.add(webinar.id)
                        global_count_t27_added += 1; weekly_count_t27 += 1; slots_filled_this_week += 1; added_in_fill = True
                        print(f"  +Fill T27 (G:{global_count_t27_added}/{target_t27}): {webinar.title[:40]}...")
                        continue
                # Пытаемся добрать T26 (если ГЛОБАЛЬНАЯ цель не достигнута)
                if slots_filled_this_week < max_webinars_per_week and global_count_t26_added < target_t26:
                    webinar = get_next_valid_webinar(available_t26)
                    if webinar:
                        webinar_weeks[webinar.id] = week_num; selected_regular_webinars.append(webinar); assigned_webinar_ids.add(webinar.id)
                        global_count_t26_added += 1; weekly_count_t26 += 1; slots_filled_this_week += 1; added_in_fill = True
                        print(f"  +Fill T26 (G:{global_count_t26_added}/{target_t26}): {webinar.title[:40]}...")
                        continue
                # Пытаемся добрать Basic (если ГЛОБАЛЬНАЯ цель не достигнута)
                if slots_filled_this_week < max_webinars_per_week and global_count_basic_added < target_basic:
                    webinar = get_next_valid_webinar(available_basic)
                    if webinar:
                        webinar_weeks[webinar.id] = week_num; selected_regular_webinars.append(webinar); assigned_webinar_ids.add(webinar.id)
                        global_count_basic_added += 1; weekly_count_basic += 1; slots_filled_this_week += 1; added_in_fill = True
                        print(f"  +Fill Bas (G:{global_count_basic_added}/{target_basic}): {webinar.title[:40]}...")
                        continue
                # Если ничего не удалось добрать
                if not added_in_fill:
                    break # Выходим из цикла добора

        print(f"Итог недели {week_num}: Добавлено {slots_filled_this_week}. T27={weekly_count_t27}, T26={weekly_count_t26}, Basic={weekly_count_basic}")

        # Проверка на общую остановку (остается как было)
        targets_met = (global_count_t27_added >= target_t27) and \
                      (global_count_t26_added >= target_t26) and \
                      (global_count_basic_added >= target_basic)
        no_more_valid_available = not any(w.id not in assigned_webinar_ids for w in available_t27) and \
                                  not any(w.id not in assigned_webinar_ids for w in available_t26) and \
                                  not any(w.id not in assigned_webinar_ids for w in available_basic)

        if targets_met and no_more_valid_available: # Останавливаемся если И цели выполнены, И больше нечего добавлять
            print("\nВсе цели достигнуты и/или доступные вебинары исчерпаны.")
            break
        elif no_more_valid_available and slots_filled_this_week == 0: # ИЛИ если вообще нечего добавлять и неделя пустая
             print("\nЗакончились все доступные вебинары для добавления.")
             break
        # Замечание: targets_met само по себе не должно останавливать цикл, т.к. мы можем
        # хотеть добавить больше по квотам, даже если глобальная цель достигнута (для баланса)
        # Остановка происходит, когда кончаются валидные вебинары.

    print(f"\nИтоги распределения:")
    print(f"Добавлено T27: {global_count_t27_added} (Цель: {target_t27})")
    print(f"Добавлено T26: {global_count_t26_added} (Цель: {target_t26})")
    print(f"Добавлено Basic: {global_count_basic_added} (Цель: {target_basic})")
    print(f"Всего добавлено Regular: {len(selected_regular_webinars)}")

    # --- 7. Сборка итогового списка ---
    result = selected_beginner_webinars + selected_regular_webinars

    # Финальная сортировка: сначала по неделе, потом по типу (Basic->T26->T27), потом по дате
    def get_category_priority(webinar):
        task_nums = {task.number for task in webinar.task_numbers}
        if 27 in task_nums: return 2
        if 26 in task_nums: return 1
        return 0 # Basic или Beginner

    result.sort(key=lambda w: (
        webinar_weeks.get(w.id, 99), # Сначала номер недели
        get_category_priority(w),    # Затем приоритет категории
        sort_key_basic(w)            # Затем дата вебинара
    ))

    print(f"\nИтоговый результат:")
    print(f"Total selected webinars: {len(result)}")
    print(f"Beginner webinars: {len(selected_beginner_webinars)}")
    print(f"Regular webinars: {len(selected_regular_webinars)}")
    # print(f"Webinar weeks dict (first 10): {dict(list(webinar_weeks.items())[:10])}")
    print("=== Конец отладки v3 ===\n")

    # Рассчитываем итоговые средние недельные квоты для возврата
    # Используем проценты, которые были финально определены
    final_quota_t27 = round(max_webinars_per_week * perc_t27)
    final_quota_t26 = round(max_webinars_per_week * perc_t26)
    final_quota_basic = max(0, max_webinars_per_week - final_quota_t27 - final_quota_t26)
    # Коррекция базовых, если сумма квот превышает лимит недели
    final_quota_basic = max(0, max_webinars_per_week - (final_quota_t27 + final_quota_t26))
    # Убедимся, что квоты не отрицательные
    final_quota_t27 = max(0, final_quota_t27)
    final_quota_t26 = max(0, final_quota_t26)


    # Возвращаем список вебинаров, словарь недель и РАССЧИТАННЫЕ КВОТЫ
    return result, webinar_weeks, final_quota_t27, final_quota_t26, final_quota_basic
