from datetime import datetime
from app.models import Webinar, WatchedWebinar, KnownTaskNumber
import math
from datetime import datetime, date

# Переносим импорт сюда
from app import db

def get_webinar_hours(webinar: Webinar) -> float:
    """Определяет "стоимость" вебинара в часах."""
    if webinar.for_beginners:
        return 2.5
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
                         is_first_plan=True, last_plan_completion_perc=0.0,
                         quota_t26=0, quota_t27=0):
    """Подбирает подходящие вебинары (v4.2 - учет часов, квоты T26/27)."""

    print("\n=== Отладка recommend_webinars v4.2 (hours, quotas) ===")
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
    print(f"Quota T26: {quota_t26}, Quota T27: {quota_t27}")

    # --- 1. Базовые параметры --- 
    hours_per_week = student.hours_per_week or 9
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
    
    # Новая логика: Откладываем только если ВСЕ условия НЕ выполнены
    # Условие 1: Последний балл >= 60 (Используем initial_score, т.к. нет поля last_mock_score)
    # Важно: Уточнить, является ли initial_score актуальным последним баллом!
    score_is_high = student.initial_score is not None and student.initial_score >= 60
    
    # Условие 2: Изучено >= 50% заданий 1-25
    tasks_1_to_25 = set(range(1, 26))
    known_tasks_1_to_25 = known_task_numbers.intersection(tasks_1_to_25)
    percentage_known_1_to_25 = (len(known_tasks_1_to_25) / 25) * 100 if tasks_1_to_25 else 0 # 25 - кол-во задач 1-25
    core_tasks_learned_enough = percentage_known_1_to_25 >= 50

    # Откладываем, только если это первый план И балл низкий И основные задачи не изучены
    should_defer = is_first_plan and not score_is_high and not core_tasks_learned_enough

    print(f"  Is first plan: {is_first_plan}")
    print(f"  Initial score: {student.initial_score}, Score >= 60: {score_is_high}")
    print(f"  Known tasks 1-25: {len(known_tasks_1_to_25)}/{len(tasks_1_to_25)} ({percentage_known_1_to_25:.1f}%), Learned >= 50%: {core_tasks_learned_enough}")
    print(f"  Should defer T26/T27: {should_defer}")

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
    
    # --- 5. Распределение регулярных вебинаров по неделям с учетом часов И КВОТ --- 
    print("\nРаспределение регулярных вебинаров по неделям:")
    total_hours_assigned_regular = 0.0
    assigned_t26_count = 0 # Счетчик добавленных T26
    assigned_t27_count = 0 # Счетчик добавленных T27

    for week_num in range(1, 6):
        print(f"\n--- Неделя {week_num} ---")
        hours_filled_this_week = weekly_hours_summary[week_num]
        
        # --- Возвращаем расчет процентных капов (активны только при quota <= 0) --- 
        apply_t26_cap = needs_task_26 and quota_t26 <= 0 
        apply_t27_cap = needs_task_27 and quota_t27 <= 0 
        max_t26_hours = 0.0
        max_t27_hours = 0.0
        if apply_t26_cap or apply_t27_cap:
             if needs_task_26 and needs_task_27:
                 # Рассчитываем, но применяем только если apply_tX_cap истинно
                 cap_value = hours_per_week * 0.25
                 max_t26_hours = cap_value if apply_t26_cap else float('inf')
                 max_t27_hours = cap_value if apply_t27_cap else float('inf')
                 print(f"  Applying caps: T26={'%.2f' % max_t26_hours if apply_t26_cap else 'off (quota)'}, T27={'%.2f' % max_t27_hours if apply_t27_cap else 'off (quota)'}")
             elif needs_task_27: 
                 cap_value = hours_per_week * 0.5
                 max_t27_hours = cap_value if apply_t27_cap else float('inf')
                 print(f"  Applying caps: T26=off, T27={'%.2f' % max_t27_hours if apply_t27_cap else 'off (quota)'}")
             elif needs_task_26: 
                 cap_value = hours_per_week * 0.5
                 max_t26_hours = cap_value if apply_t26_cap else float('inf')
                 print(f"  Applying caps: T26={'%.2f' % max_t26_hours if apply_t26_cap else 'off (quota)'}, T27=off")
        else:
             print("  Percentage caps disabled due to quotas for both T26 and T27.")
        # Часы, уже потраченные на T26/T27 в этой неделе (для проверки капа)
        current_t26_hours_this_week = 0.0
        current_t27_hours_this_week = 0.0
        # --- Конец расчета капов ---

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
            added_in_this_attempt = False

            # --- Попытка 1: Добавить T27 --- 
            should_try_t27 = assigned_t27_count < quota_t27 or quota_t27 <= 0
            webinar_t27 = get_next_valid_webinar(available_t27)
            if should_try_t27 and webinar_t27:
                if webinar_t27.id in assigned_webinar_ids: # Доп. проверка на всякий случай
                    print(f"  ! Warning: T27 {webinar_t27.id} уже был назначен, пропускаем")
                    continue # Переходим к след итерации while
                w_hours = get_webinar_hours(webinar_t27)
                budget_fits = hours_filled_this_week + w_hours <= hours_per_week
                
                # --- Измененная проверка капа T27 --- 
                cap_check = apply_t27_cap and max_t27_hours > 0
                is_first_t27_this_week = current_t27_hours_this_week == 0.0
                # Кап превышен, если он активен, И сумма превышает кап, И это НЕ первый T27 вебинар в неделе
                cap_exceeded = cap_check and (current_t27_hours_this_week + w_hours > max_t27_hours) and not is_first_t27_this_week
                # --- Конец проверки капа T27 --- 
                
                if budget_fits and not cap_exceeded: 
                    # Добавляем T27
                    webinar_weeks[webinar_t27.id] = week_num
                    selected_regular_webinars.append(webinar_t27)
                    assigned_webinar_ids.add(webinar_t27.id)
                    hours_filled_this_week += w_hours
                    total_hours_assigned_regular += w_hours
                    current_t27_hours_this_week += w_hours # Обновляем часы для капа
                    assigned_t27_count += 1 # Увеличиваем счетчик добавленных T27
                    added_in_this_attempt = True
                    print(f"  + Add T27 ({w_hours:.1f}h): {webinar_t27.title[:40]}... (Week total: {hours_filled_this_week:.1f}h)")
                    # Не возвращаем в available_t27
                else:
                    # Не добавили T27 - возвращаем в список и выводим сообщение (если не кап)
                    available_t27.insert(0, webinar_t27)
                    if not budget_fits:
                         print(f"  - Skip T27 ({w_hours:.1f}h) - not enough budget (Rem: {(hours_per_week - hours_filled_this_week):.1f}h)")
                    elif cap_exceeded:
                         print(f"  - Skip T27 ({w_hours:.1f}h) - exceeds cap ({max_t27_hours:.2f}h) for T27 this week (Current T27:{current_t27_hours_this_week:.1f}h)")
            
            elif webinar_t27: # Если НЕ должны были пытаться добавить T27 (квота выполнена), но вебинар есть
                available_t27.insert(0, webinar_t27) # Возвращаем обратно
            
            # --- Попытка 2: Добавить T26 --- 
            should_try_t26 = assigned_t26_count < quota_t26 or quota_t26 <= 0
            if not added_in_this_attempt and should_try_t26:
                webinar_t26 = get_next_valid_webinar(available_t26)
                if webinar_t26:
                    if webinar_t26.id in assigned_webinar_ids: continue # Пропускаем уже добавленные
                    w_hours = get_webinar_hours(webinar_t26)
                    budget_fits = hours_filled_this_week + w_hours <= hours_per_week
                    
                    # --- Измененная проверка капа T26 --- 
                    cap_check = apply_t26_cap and max_t26_hours > 0
                    is_first_t26_this_week = current_t26_hours_this_week == 0.0
                    cap_exceeded = cap_check and (current_t26_hours_this_week + w_hours > max_t26_hours) and not is_first_t26_this_week
                    # --- Конец проверки капа T26 --- 
                    
                    if budget_fits and not cap_exceeded: 
                        # Добавляем T26
                        webinar_weeks[webinar_t26.id] = week_num
                        selected_regular_webinars.append(webinar_t26)
                        assigned_webinar_ids.add(webinar_t26.id)
                        hours_filled_this_week += w_hours
                        total_hours_assigned_regular += w_hours
                        current_t26_hours_this_week += w_hours # Обновляем часы для капа
                        assigned_t26_count += 1 # Увеличиваем счетчик добавленных T26
                        added_in_this_attempt = True
                        print(f"  + Add T26 ({w_hours:.1f}h): {webinar_t26.title[:40]}... (Week total: {hours_filled_this_week:.1f}h)")
                        # Не возвращаем в available_t26
                    else:
                        # Не добавили T26 - возвращаем в список
                        available_t26.insert(0, webinar_t26)
                        if not budget_fits:
                            print(f"  - Skip T26 ({w_hours:.1f}h) - not enough budget (Rem: {(hours_per_week - hours_filled_this_week):.1f}h)")
                            # Если T26 не влез по бюджету, то дальше точно ничего не влезет
                            print("    (T26 didn't fit budget, ending week fill.)")
                            break # Прерываем WHILE для этой недели
                # else: 
                    # Если T26 не найден (available_t26 пуст) - ничего не делаем,
                    # added_in_this_attempt останется False, сработает проверка ниже.
            
            # --- Попытка 3: Добавить Basic --- 
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

    print(f"\nAssigned T26: {assigned_t26_count} (quota: {quota_t26})")
    print(f"Assigned T27: {assigned_t27_count} (quota: {quota_t27})")
    print(f"\n=== Конец recommend_webinars ===")
    # Объединяем beginner и regular вебинары для возврата
    all_selected_webinars = selected_beginner_webinars + selected_regular_webinars
    print(f"Total webinars selected: {len(all_selected_webinars)}")
    print(f"Weekly hours summary: {weekly_hours_summary}")
    
    # Возвращаем три значения
    return all_selected_webinars, webinar_weeks, weekly_hours_summary
