from datetime import datetime
from app.models import Webinar, WatchedWebinar, KnownTaskNumber
import math
from datetime import datetime, date

# Переносим импорт сюда
from app import db

def get_webinar_hours(webinar: Webinar) -> float:
    """Определяет "стоимость" вебинара в часах."""
    if webinar.for_beginners:
        return 1.5
    elif webinar.for_advanced or webinar.for_expert:
        return 4.0
    # По умолчанию (включая for_basic, for_mocks, for_practice, for_minisnap и без флагов)
    return 3.0

def get_next_valid_webinar(webinar_list):
    """Извлекает первый вебинар из списка, если он не пуст."""
    if webinar_list:
        return webinar_list.pop(0)
    return None


def recommend_webinars(student, known_task_numbers, watched_webinar_ids,
                         is_first_plan=True, last_plan_completion_perc=0.0):
    """Подбирает подходящие вебинары (v4.1 - учет часов, кап 50%, отложенные T26/27)."""

    print("\n=== Отладка recommend_webinars v4.1 (hours, cap) ===")
    print(f"Student ID: {student.id}")
    # print(f"Task 26 deferred (start): {student.task_26_deferred}") # Атрибут удален
    # print(f"Task 27 deferred (start): {student.task_27_deferred}") # Атрибут удален
    print(f"Needs Python Basics: {student.needs_python_basics}")
    print(f"Initial score: {student.initial_score}")
    print(f"Target score: {student.target_score}")
    print(f"Hours per week: {student.hours_per_week}")
    print(f"Is First Plan: {is_first_plan}")
    print(f"Last Plan Completion: {last_plan_completion_perc*100:.1f}%")
    print(f"Known tasks: {known_task_numbers}")
    print(f"Watched webinars: {len(watched_webinar_ids)}")

    # --- 1. Базовые параметры --- 
    hours_per_week = student.hours_per_week or 9 # Бюджет часов в неделю (минимум 9 по умолчанию)
    print("\nБазовые параметры:")
    print(f"Weekly hours budget: {hours_per_week}")

    webinar_weeks = {} # Словарь для хранения недели каждого вебинара {webinar_id: week_num}
    weekly_hours_summary = {w: 0.0 for w in range(1, 6)} # Часы по неделям
    selected_beginner_webinars = [] # Отдельно для beginner (всегда в Неделю 1)
    selected_regular_webinars = []  # Для всех остальных вебинаров
    assigned_webinar_ids = set() # Чтобы не дублировать вебинары

    # --- 2. Обработка "Python с нуля" --- 
    beginner_hours_filled_week1 = 0.0
    remaining_beginner_webinars_overflow = [] # Список beginner вебинаров, не влезших в 1 неделю
    
    # Загружаем все вебинары один раз
    all_webinars = Webinar.query.options(db.joinedload(Webinar.task_numbers)).all()

    if student.needs_python_basics:
        beginner_webinars_available = [w for w in all_webinars if w.for_beginners and w.id not in watched_webinar_ids]
        print(f"\nНайдено доступных beginner вебинаров: {len(beginner_webinars_available)}")
        # Добавляем beginner вебинары, пока не превысим бюджет 1-й недели
        hours_filled_week1 = 0.0
        for w in beginner_webinars_available:
            if w.id in assigned_webinar_ids: continue # Пропускаем уже добавленные
            w_hours = get_webinar_hours(w)
            if hours_filled_week1 + w_hours <= hours_per_week:
                webinar_weeks[w.id] = 1 # Всегда в 1 неделю
                selected_beginner_webinars.append(w)
                assigned_webinar_ids.add(w.id)
                hours_filled_week1 += w_hours
            else:
                remaining_beginner_webinars_overflow.append(w) # Сохраняем для недели 2

        print(f"Добавлено beginner (Неделя 1): {len(selected_beginner_webinars)} вебинаров ({hours_filled_week1} часов)")
        print(f"Осталось beginner для Недели 2: {len(remaining_beginner_webinars_overflow)} вебинаров")
        weekly_hours_summary[1] = hours_filled_week1 # Записываем часы 1-й недели
    else:
        print("\nPython Basics не требуется.")
        
    # Удаляем beginner вебинары из дальнейшего рассмотрения (включая overflow)
    regular_webinars = [w for w in all_webinars if not w.for_beginners]

    # --- 3. Определение необходимых заданий и ФИЛЬТРАЦИЯ вебинаров --- 
    required_tasks = set()
    needs_task_26 = False
    needs_task_27 = False

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
    else: # Если балл не указан, берем базу до 90
         required_tasks = tasks_85_90.copy()

    # --- ДОБАВЛЯЕМ ЛОГИКУ ОТКЛАДЫВАНИЯ --- 
    print(f"\nПроверка на откладывание T26/T27:")
    should_defer = is_first_plan and (student.initial_score is None or student.initial_score <= 40)
    print(f"  Is first plan: {is_first_plan}, Initial score: {student.initial_score}, Should defer: {should_defer}")
    if should_defer:
        deferred_26 = 26 in required_tasks
        deferred_27 = 27 in required_tasks
        if deferred_26:
            required_tasks.discard(26)
            print("  - Task 26 deferred for this plan.")
        if deferred_27:
            required_tasks.discard(27)
            print("  - Task 27 deferred for this plan.")
    # --- КОНЕЦ ЛОГИКИ ОТКЛАДЫВАНИЯ --- 

    # Удаляем известные задания ИЗ required_tasks
    if known_task_numbers:
        print(f"Удаление известных заданий {known_task_numbers} из required_tasks.")
        required_tasks.difference_update(known_task_numbers)
        
    needs_task_26 = 26 in required_tasks
    needs_task_27 = 27 in required_tasks

    print(f"\nИтоговые параметры для плана:")
    print(f"Required tasks (final): {sorted(list(required_tasks))}")
    print(f"Needs task 26: {needs_task_26}")
    print(f"Needs task 27: {needs_task_27}")

    # Фильтрация регулярных вебинаров
    available_regular = []
    print(f"\nФильтрация регулярных вебинаров (проверка по required_tasks):")
    for w in regular_webinars:
        if w.id in assigned_webinar_ids or w.id in watched_webinar_ids: continue # Пропускаем уже добавленные или просмотренные
        if not w.task_numbers: continue # Пропускаем вебинары без заданий
        webinar_tasks = {t.number for t in w.task_numbers}
        
        # Пропускаем, если состоит ТОЛЬКО из известных
        if known_task_numbers and webinar_tasks.issubset(known_task_numbers):
            print(f"  - Skip (all tasks known {webinar_tasks}): {w.title[:60]}...")
            continue
            
        # Пропускаем, если НЕТ пересечения с нужными заданиями
        if not webinar_tasks.intersection(required_tasks):
            print(f"  - Skip (no required tasks {webinar_tasks}): {w.title[:60]}...")
            continue
            
        # Пропускаем 26/27, если они не нужны
        if 26 in webinar_tasks and not needs_task_26:
            print(f"  - Skip (Task 26 not needed): {w.title[:60]}...")
            continue
        if 27 in webinar_tasks and not needs_task_27:
            print(f"  - Skip (Task 27 not needed): {w.title[:60]}...")
            continue
            
        available_regular.append(w)
        # print(f"  + Keep: {w.title[:60]}...")

    print(f"Доступно регулярных вебинаров после фильтрации: {len(available_regular)}")

    # --- 4. Категоризация и сортировка доступных регулярных вебинаров --- 
    available_basic = []
    available_t26 = []
    available_t27 = []

    for webinar in available_regular:
        task_nums = {task.number for task in webinar.task_numbers}
        is_task_26 = 26 in task_nums
        is_task_27 = 27 in task_nums
        if is_task_27 and needs_task_27:
            available_t27.append(webinar)
        elif is_task_26 and needs_task_26:
            available_t26.append(webinar)
        else:
            available_basic.append(webinar)

    print(f"\nКатегоризация доступных регулярных:")
    print(f"Task 27 : {len(available_t27)}")
    print(f"Task 26 : {len(available_t26)}")
    print(f"Basic   : {len(available_basic)}")
    
    # Сортировка внутри категорий (например, по дате)
    # --- ИЗМЕНЕННАЯ СОРТИРОВКА T27 --- 
    def sort_key_t27(webinar):
        is_cluster = 1 # По умолчанию не кластер
        if webinar.title and "кластер" in webinar.title.lower():
            is_cluster = 0 # Кластеры идут первыми
        
        dt_obj = None
        if webinar.date:
            if isinstance(webinar.date, datetime): dt_obj = webinar.date
            elif isinstance(webinar.date, date): dt_obj = datetime.combine(webinar.date, datetime.min.time())
        
        if dt_obj: 
            return (is_cluster, 0, dt_obj.replace(tzinfo=None))
        return (is_cluster, 1, datetime(2000, 1, 1)) # Сначала кластеры, потом по дате (сначала с датой)
        
    def sort_key_date(webinar):
         dt_obj = None
         if webinar.date:
             if isinstance(webinar.date, datetime): dt_obj = webinar.date
             elif isinstance(webinar.date, date): dt_obj = datetime.combine(webinar.date, datetime.min.time())
         if dt_obj: return (0, dt_obj.replace(tzinfo=None))
         return (1, datetime(2000, 1, 1))

    available_t27.sort(key=sort_key_t27)
    available_t26.sort(key=sort_key_date)
    available_basic.sort(key=sort_key_date)
    
    # --- 5. Распределение регулярных вебинаров по неделям с учетом часов --- 
    print("\nРаспределение регулярных вебинаров по неделям:")
    total_hours_assigned_regular = 0.0

    for week_num in range(1, 6):
        print(f"\n--- Неделя {week_num} ---")
        # Начинаем с часов, уже занятых beginner в 1й неделе
        hours_filled_this_week = weekly_hours_summary[week_num]
        t26_hours_this_week = 0.0 # Часы T26 в этой неделе для капа
        t27_hours_this_week = 0.0 # Часы T27 в этой неделе для капа
        
        # --- Новая логика расчета капов для текущей недели ---
        max_t26_hours = 0.0
        max_t27_hours = 0.0
        if needs_task_26 and needs_task_27:
            max_t26_hours = hours_per_week * 0.25
            max_t27_hours = hours_per_week * 0.25
            print(f"  Applying 25% cap for T26 ({max_t26_hours:.1f}h) and T27 ({max_t27_hours:.1f}h)")
        elif needs_task_27: # Только T27
            max_t27_hours = hours_per_week * 0.5
            print(f"  Applying 50% cap for T27 ({max_t27_hours:.1f}h)")
        elif needs_task_26: # Только T26
            max_t26_hours = hours_per_week * 0.5
            print(f"  Applying 50% cap for T26 ({max_t26_hours:.1f}h)")
        # --- Конец новой логики капов ---

        # Добавляем оставшиеся beginner вебинары во 2-ю неделю
        if week_num == 2 and remaining_beginner_webinars_overflow:
            print(f"  Добавляем overflow beginner ({len(remaining_beginner_webinars_overflow)} шт.)")
            # Делаем копию и очищаем оригинал, чтобы избежать бесконечного цикла при нехватке бюджета
            overflow_to_process = remaining_beginner_webinars_overflow[:]
            remaining_beginner_webinars_overflow.clear()
            for w in overflow_to_process:
                if w.id in assigned_webinar_ids: continue
                w_hours = get_webinar_hours(w)
                if hours_filled_this_week + w_hours <= hours_per_week:
                     webinar_weeks[w.id] = week_num
                     selected_beginner_webinars.append(w) # Все еще считаем их beginner
                     assigned_webinar_ids.add(w.id)
                     hours_filled_this_week += w_hours
                     print(f"    + Add Overflow Beginner ({w_hours:.1f}h): {w.title[:40]}... (Week total: {hours_filled_this_week:.1f}h)")
                else:
                     print(f"    - Skip Overflow Beginner ({w_hours:.1f}h) - not enough budget. Вебинар потерян.")
                     # Не добавляем обратно в overflow, чтобы избежать зацикливания
            weekly_hours_summary[week_num] = hours_filled_this_week # Обновляем часы после overflow

        # Заполняем неделю, пока есть бюджет и доступные вебинары
        while hours_filled_this_week < hours_per_week:
            added_in_this_attempt = False # Флаг, что удалось добавить ХОТЬ ЧТО-ТО на этой ПОПЫТКЕ (T27/T26/Bas)

            # --- Попытка 1: Добавить T27 ---
            webinar_t27 = get_next_valid_webinar(available_t27)
            if webinar_t27:
                if webinar_t27.id in assigned_webinar_ids: # Доп. проверка на всякий случай
                    print(f"  ! Warning: T27 {webinar_t27.id} уже был назначен, пропускаем")
                    continue # Переходим к след итерации while
                w_hours = get_webinar_hours(webinar_t27)
                cap_exceeded = False
                # Проверяем новый кап для T27
                if max_t27_hours > 0 and t27_hours_this_week + w_hours > max_t27_hours:
                    cap_exceeded = True
                    print(f"  - Skip T27 ({w_hours:.1f}h) - exceeds cap ({max_t27_hours:.1f}h) for T27 this week (Current T27:{t27_hours_this_week:.1f}h)")
                
                budget_fits = hours_filled_this_week + w_hours <= hours_per_week

                if not cap_exceeded and budget_fits:
                    # Добавляем T27
                    webinar_weeks[webinar_t27.id] = week_num
                    selected_regular_webinars.append(webinar_t27)
                    assigned_webinar_ids.add(webinar_t27.id)
                    hours_filled_this_week += w_hours
                    total_hours_assigned_regular += w_hours
                    t27_hours_this_week += w_hours
                    added_in_this_attempt = True
                    print(f"  + Add T27 ({w_hours:.1f}h): {webinar_t27.title[:40]}... (Week total: {hours_filled_this_week:.1f}h)")
                    # Не возвращаем в available_t27
                else:
                    # Не добавили T27 - возвращаем в список и выводим сообщение (если не кап)
                    available_t27.insert(0, webinar_t27)
                    if not cap_exceeded:
                         print(f"  - Skip T27 ({w_hours:.1f}h) - not enough budget (Rem: {(hours_per_week - hours_filled_this_week):.1f}h)")
                    # НЕ ставим added_in_this_attempt = True, продолжаем проверять T26/Bas
            
            # --- Попытка 2: Добавить T26 (только если T27 не добавили на этой попытке) ---
            if not added_in_this_attempt:
                webinar_t26 = get_next_valid_webinar(available_t26)
                if webinar_t26:
                    if webinar_t26.id in assigned_webinar_ids: continue # Пропускаем уже добавленные
                    w_hours = get_webinar_hours(webinar_t26)
                    cap_exceeded = False
                    # Проверяем новый кап для T26
                    if max_t26_hours > 0 and t26_hours_this_week + w_hours > max_t26_hours:
                        cap_exceeded = True
                        print(f"  - Skip T26 ({w_hours:.1f}h) - exceeds cap ({max_t26_hours:.1f}h) for T26 this week (Current T26:{t26_hours_this_week:.1f}h)")
                    
                    budget_fits = hours_filled_this_week + w_hours <= hours_per_week
                    
                    if not cap_exceeded and budget_fits:
                        # Добавляем T26
                        webinar_weeks[webinar_t26.id] = week_num
                        selected_regular_webinars.append(webinar_t26)
                        assigned_webinar_ids.add(webinar_t26.id)
                        hours_filled_this_week += w_hours
                        total_hours_assigned_regular += w_hours
                        t26_hours_this_week += w_hours
                        added_in_this_attempt = True
                        print(f"  + Add T26 ({w_hours:.1f}h): {webinar_t26.title[:40]}... (Week total: {hours_filled_this_week:.1f}h)")
                        # Не возвращаем в available_t26
                    else:
                        # Не добавили T26 - возвращаем в список
                        available_t26.insert(0, webinar_t26)
                        if not cap_exceeded:
                            print(f"  - Skip T26 ({w_hours:.1f}h) - not enough budget (Rem: {(hours_per_week - hours_filled_this_week):.1f}h)")
                        # НЕ ставим added_in_this_attempt = True, продолжаем проверять Basic
            
            # --- Попытка 3: Добавить Basic (только если T27 и T26 не добавили на этой попытке) ---
            if not added_in_this_attempt:
                 webinar_basic = get_next_valid_webinar(available_basic)
                 if webinar_basic:
                     if webinar_basic.id in assigned_webinar_ids: continue # Пропускаем уже добавленные
                     w_hours = get_webinar_hours(webinar_basic)
                     # Капа для Basic нет
                     budget_fits = hours_filled_this_week + w_hours <= hours_per_week
                     
                     if budget_fits:
                         # Добавляем Basic
                         webinar_weeks[webinar_basic.id] = week_num
                         selected_regular_webinars.append(webinar_basic)
                         assigned_webinar_ids.add(webinar_basic.id)
                         hours_filled_this_week += w_hours
                         total_hours_assigned_regular += w_hours
                         # Часы T26/T27 для капа не меняются
                         added_in_this_attempt = True
                         print(f"  + Add Bas ({w_hours:.1f}h): {webinar_basic.title[:40]}... (Week total: {hours_filled_this_week:.1f}h)")
                         # Не возвращаем в available_basic
                     else:
                         # Не добавили Basic - возвращаем в список
                         available_basic.insert(0, webinar_basic)
                         print(f"  - Skip Bas ({w_hours:.1f}h) - not enough budget (Rem: {(hours_per_week - hours_filled_this_week):.1f}h)")
                         # Если Basic не влез по бюджету, то дальше точно ничего не влезет
                         print("    (Basic didn't fit budget, ending week fill.)")
                         break # Прерываем WHILE для этой недели
                 # else: 
                     # Если Basic не найден (available_basic пуст) - ничего не делаем,
                     # added_in_this_attempt останется False, сработает проверка ниже.
                         
            # --- Проверка после всех попыток на этой итерации --- 
            # Если после попыток добавить T27, T26 и Basic НИЧЕГО не было добавлено,
            # значит либо доступных вебинаров нет, либо оставшийся бюджет слишком мал.
            if not added_in_this_attempt:
                 print("  -> Nothing could be added in this attempt (no suitable webinars or budget left), ending week fill.")
                 break # Прерываем WHILE для этой недели

        # Записываем итоговые часы для текущей недели
        weekly_hours_summary[week_num] = hours_filled_this_week

    print(f"\n=== Конец recommend_webinars ===")
    # Объединяем beginner и regular вебинары для возврата
    all_selected_webinars = selected_beginner_webinars + selected_regular_webinars
    print(f"Total webinars selected: {len(all_selected_webinars)}")
    print(f"Weekly hours summary: {weekly_hours_summary}")
    
    # Возвращаем три значения
    return all_selected_webinars, webinar_weeks, weekly_hours_summary
