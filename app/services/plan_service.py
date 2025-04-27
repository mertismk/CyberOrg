from datetime import datetime, date
from collections import deque, Counter  # Добавляем Counter

# Переносим импорт сюда
from app import db
from app.models import Webinar  # Добавляем этот импорт

# Определяем примерную длительность Т26/Т27 для логики капов
T26_T27_APPROX_HOURS = 4.0


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
        return T26_T27_APPROX_HOURS
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


def _group_and_sort_by_task(available_regular, required_tasks):
    """Группирует вебинары по задачам и сортирует их внутри групп."""
    webinars_by_task = {task_num: [] for task_num in required_tasks}
    for webinar in available_regular:
        webinar_tasks_covered = {t.number for t in webinar.task_numbers}
        relevant_tasks = webinar_tasks_covered.intersection(required_tasks)
        for task_num in relevant_tasks:
            webinars_by_task[task_num].append(webinar)

    task_deques = {}
    print("\nГруппировка и сортировка вебинаров по задачам:")
    for task_num in sorted(list(required_tasks)):
        webinar_list = webinars_by_task.get(task_num, [])
        # Убираем дубликаты вебинаров внутри одной задачи (если они как-то попали)
        unique_webinars = list({w.id: w for w in webinar_list}.values())
        if unique_webinars:
            unique_webinars.sort(key=create_webinar_sort_key)
            task_deques[task_num] = deque(unique_webinars)
            print(f"  Task {task_num}: {len(task_deques[task_num])} webinars sorted.")
        else:
            print(f"  Task {task_num}: No available webinars found.")

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
    """Распределяет вебинары по неделям, с приоритетным заполнением слотов T27/T26."""
    webinar_weeks = {}
    selected_regular_webinars = []
    total_t26_added = 0
    total_t27_added = 0

    # Рассчитываем бюджеты слотов и строгие капы (если квоты не заданы)
    cap_percentage = 0.35
    t27_budget_slot = hours_per_week * cap_percentage
    t26_budget_slot = hours_per_week * cap_percentage
    strict_max_t26_hours = t26_budget_slot if quota_t26 <= 0 else float("inf")
    strict_max_t27_hours = t27_budget_slot if quota_t27 <= 0 else float("inf")

    print(
        f"\nWeekly Budgets: Total={hours_per_week:.2f}, T27 Slot={t27_budget_slot:.2f}, T26 Slot={t26_budget_slot:.2f}"
    )
    print(
        f"Strict Caps: T26={strict_max_t26_hours:.2f}, T27={strict_max_t27_hours:.2f}"
    )

    print("\nРаспределение вебинаров по неделям (3 фазы):")
    for week_num in range(1, 5):
        print(f"\n--- Неделя {week_num} ---")
        hours_filled_this_week = weekly_hours_summary[week_num]
        current_t27_hours_this_week = 0.0
        current_t26_hours_this_week = 0.0

        # Добавляем overflow beginner на 2-й неделе (остается без изменений)
        if week_num == 2 and remaining_beginner_overflow:
            print(
                f"  Phase 0: Добавляем overflow beginner ({len(remaining_beginner_overflow)} шт.)"
            )
            while remaining_beginner_overflow:
                w_overflow = remaining_beginner_overflow[0]
                if w_overflow.id in assigned_webinar_ids:
                    remaining_beginner_overflow.popleft()
                    continue
                w_hours = get_webinar_hours(w_overflow)
                if hours_filled_this_week + w_hours <= hours_per_week:
                    w_to_add = remaining_beginner_overflow.popleft()
                    webinar_weeks[w_to_add.id] = week_num
                    assigned_webinar_ids.add(w_to_add.id)
                    hours_filled_this_week += w_hours
                    print(
                        f"    + Added Overflow Beginner ID: {w_to_add.id} ({w_hours:.1f}h). Week total: {hours_filled_this_week:.1f}h"
                    )
                else:
                    print(
                        f"    - Skip Overflow Beginner ID: {w_overflow.id} ({w_hours:.1f}h) - not enough budget."
                    )
                    remaining_beginner_overflow.clear()
                    break
            weekly_hours_summary[week_num] = hours_filled_this_week

        # --- Фаза 1: Заполнение слота T27 ---
        print(f"  Phase 1: T27 Slot (Target: {t27_budget_slot:.1f}h)")
        t27_deque = task_deques.get(27)
        # Счетчик для отслеживания количества T27 вебинаров, добавленных за текущую неделю
        weekly_t27_added = (
            0  # ДОБАВЛЕНО: недельный счетчик (вместо глобального total_t27_added)
        )

        while t27_deque and hours_filled_this_week < hours_per_week:
            if not t27_deque:  # Доп. проверка, если очередь опустела
                break
            candidate = t27_deque[0]
            candidate_hours = get_webinar_hours(candidate)

            if candidate.id in assigned_webinar_ids:
                t27_deque.popleft()
                continue

            # --- ДОБАВЛЕНО: Проверка на превышение общего недельного бюджета ---
            if hours_filled_this_week + candidate_hours > hours_per_week:
                print(
                    f"    - Skip T27 ID: {candidate.id} ({candidate_hours:.1f}h) - exceeds weekly budget {hours_per_week:.1f}h (current: {hours_filled_this_week:.1f}h)"
                )
                break  # Не помещается в общий бюджет, выходим из фазы T27
            # --- КОНЕЦ ДОБАВЛЕНИЯ ---

            # --- ИЗМЕНЕНО: Проверка на превышение ЕЖЕНЕДЕЛЬНОЙ квоты ---
            if quota_t27 > 0 and weekly_t27_added >= quota_t27:
                print(
                    f"    - Skip T27 ID: {candidate.id} - Weekly T27 quota ({quota_t27}) reached for week {week_num}."
                )
                break  # Квота на эту неделю достигнута, выходим из фазы T27
            # --- КОНЕЦ ИЗМЕНЕНИЯ ---

            # Добавляем вебинар T27
            webinar_to_add = t27_deque.popleft()
            webinar_weeks[webinar_to_add.id] = week_num
            selected_regular_webinars.append(webinar_to_add)
            assigned_webinar_ids.add(webinar_to_add.id)
            hours_filled_this_week += candidate_hours
            current_t27_hours_this_week += candidate_hours
            total_t27_added += 1
            weekly_t27_added += 1  # ДОБАВЛЕНО: увеличиваем недельный счетчик
            print(
                f"    + Added T27 ID: {webinar_to_add.id} ({candidate_hours:.1f}h). Week T27: {current_t27_hours_this_week:.1f}h. Week total: {hours_filled_this_week:.1f}h. Week T27 count: {weekly_t27_added}, Total T27 added: {total_t27_added}"
            )

        # --- Фаза 2: Заполнение слота T26 ---
        print(f"  Phase 2: T26 Slot (Target: {t26_budget_slot:.1f}h)")
        t26_deque = task_deques.get(26)
        # Счетчик для отслеживания количества T26 вебинаров, добавленных за текущую неделю
        weekly_t26_added = (
            0  # ДОБАВЛЕНО: недельный счетчик (вместо глобального total_t26_added)
        )

        while t26_deque and hours_filled_this_week < hours_per_week:
            if not t26_deque:
                break
            candidate = t26_deque[0]
            candidate_hours = get_webinar_hours(candidate)

            if candidate.id in assigned_webinar_ids:
                t26_deque.popleft()
                continue

            # --- ДОБАВЛЕНО: Проверка на превышение общего недельного бюджета ---
            if hours_filled_this_week + candidate_hours > hours_per_week:
                print(
                    f"    - Skip T26 ID: {candidate.id} ({candidate_hours:.1f}h) - exceeds weekly budget {hours_per_week:.1f}h (current: {hours_filled_this_week:.1f}h)"
                )
                break  # Не помещается в общий бюджет, выходим из фазы T26
            # --- КОНЕЦ ДОБАВЛЕНИЯ ---

            # --- ИЗМЕНЕНО: Проверка на превышение ЕЖЕНЕДЕЛЬНОЙ квоты ---
            if quota_t26 > 0 and weekly_t26_added >= quota_t26:
                print(
                    f"    - Skip T26 ID: {candidate.id} - Weekly T26 quota ({quota_t26}) reached for week {week_num}."
                )
                break  # Квота на эту неделю достигнута, выходим из фазы T26
            # --- КОНЕЦ ИЗМЕНЕНИЯ ---

            # Добавляем вебинар T26
            webinar_to_add = t26_deque.popleft()
            webinar_weeks[webinar_to_add.id] = week_num
            selected_regular_webinars.append(webinar_to_add)
            assigned_webinar_ids.add(webinar_to_add.id)
            hours_filled_this_week += candidate_hours
            current_t26_hours_this_week += candidate_hours
            total_t26_added += 1
            weekly_t26_added += 1  # ДОБАВЛЕНО: увеличиваем недельный счетчик
            print(
                f"    + Added T26 ID: {webinar_to_add.id} ({candidate_hours:.1f}h). Week T26: {current_t26_hours_this_week:.1f}h. Week total: {hours_filled_this_week:.1f}h. Week T26 count: {weekly_t26_added}, Total T26 added: {total_t26_added}"
            )

        # --- Фаза 3: Заполнение остатка недели ---
        print(
            f"  Phase 3: Filling Remaining Budget ({(hours_per_week - hours_filled_this_week):.1f}h left)"
        )
        while hours_filled_this_week < hours_per_week:
            added_in_this_iteration = False  # Флаг, показывающий, добавили ли мы что-то

            # --- Шаг 3.1: Поиск лучшего кандидата из задач 1-25 ---
            best_candidate_1_to_25 = None
            best_task_num_1_to_25 = -1
            best_sort_key_1_to_25 = (
                float("inf"),
                (float("inf"), datetime.max),
                float("inf"),
            )

            # Собираем активные очереди только для задач 1-25
            active_tasks_1_to_25 = {
                k: v
                for k, v in task_deques.items()
                if v and 1 <= k <= 25  # Только непустые очереди в диапазоне 1-25
            }

            if active_tasks_1_to_25:  # Искать только если есть активные задачи 1-25
                candidate_search_restart_needed = (
                    False  # Флаг для перезапуска внутреннего поиска 1-25
                )
                while (
                    True
                ):  # Цикл для перезапуска поиска 1-25, если удалили уже добавленный
                    best_candidate_1_to_25_inner = None
                    best_task_num_1_to_25_inner = -1
                    best_sort_key_1_to_25_inner = (
                        float("inf"),
                        (float("inf"), datetime.max),
                        float("inf"),
                    )

                    for task_num, task_deque in active_tasks_1_to_25.items():
                        if not task_deque:
                            continue

                        candidate = task_deque[0]
                        candidate_hours = get_webinar_hours(candidate)

                        # 1. Проверка: Уже добавлен?
                        if candidate.id in assigned_webinar_ids:
                            task_deque.popleft()
                            candidate_search_restart_needed = (
                                True  # Нужен перезапуск внешнего цикла
                            )
                            best_candidate_1_to_25_inner = (
                                None  # Сбрасываем кандидата для этого цикла
                            )
                            break  # Выходим из for, чтобы перезапустить while True

                        # 2. Проверка: Помещается ли в общий бюджет?
                        if hours_filled_this_week + candidate_hours > hours_per_week:
                            continue

                        # 3. Сравнение с текущим лучшим (в рамках 1-25)
                        candidate_sort_key = create_webinar_sort_key(candidate)
                        if candidate_sort_key < best_sort_key_1_to_25_inner:
                            best_candidate_1_to_25_inner = candidate
                            best_task_num_1_to_25_inner = task_num
                            best_sort_key_1_to_25_inner = candidate_sort_key

                    if candidate_search_restart_needed:
                        candidate_search_restart_needed = False  # Сбросили флаг
                        active_tasks_1_to_25 = {
                            k: v for k, v in active_tasks_1_to_25.items() if v
                        }  # Обновляем активные очереди
                        if (
                            not active_tasks_1_to_25
                        ):  # Если все очереди 1-25 опустели из-за popleft
                            break  # Выходим из while True
                        continue  # Перезапускаем поиск 1-25
                    else:
                        # Если поиск завершился без необходимости перезапуска
                        best_candidate_1_to_25 = best_candidate_1_to_25_inner
                        best_task_num_1_to_25 = best_task_num_1_to_25_inner
                        best_sort_key_1_to_25 = best_sort_key_1_to_25_inner
                        break  # Выходим из while True

            # --- Шаг 3.2: Добавление лучшего кандидата 1-25, если найден и подходит ---
            if best_candidate_1_to_25:
                candidate_hours = get_webinar_hours(best_candidate_1_to_25)
                if hours_filled_this_week + candidate_hours <= hours_per_week:
                    webinar_to_add = task_deques[best_task_num_1_to_25].popleft()
                    if webinar_to_add.id not in assigned_webinar_ids:
                        w_hours = candidate_hours
                        webinar_weeks[webinar_to_add.id] = week_num
                        selected_regular_webinars.append(webinar_to_add)
                        assigned_webinar_ids.add(webinar_to_add.id)
                        hours_filled_this_week += w_hours
                        added_in_this_iteration = True
                        print(
                            f"    + Added Other (1-25) ID: {webinar_to_add.id} (Task {best_task_num_1_to_25}, {w_hours:.1f}h). Week total: {hours_filled_this_week:.1f}h."
                        )
                        # --- Переходим к следующей итерации основного цикла while ---
                        continue
                    else:
                        print(
                            f"!!! WARNING: Trying to re-add webinar {webinar_to_add.id} (1-25) in Phase 3, skipping."
                        )
                        # added_in_this_iteration остается False, пробуем T26/T27
                # else: Бюджет не позволяет добавить лучший 1-25, переходим к T26/T27

            # --- Шаг 3.3: Если НЕ добавили 1-25, ищем лучший из T26/T27 ---
            if not added_in_this_iteration:
                best_candidate_t26_t27 = None
                best_task_num_t26_t27 = -1
                best_sort_key_t26_t27 = (
                    float("inf"),
                    (float("inf"), datetime.max),
                    float("inf"),
                )

                active_tasks_t26_t27 = {
                    k: v for k, v in task_deques.items() if v and k in [26, 27]
                }

                if active_tasks_t26_t27:
                    candidate_search_restart_needed_t26_t27 = False
                    while True:
                        best_candidate_t26_t27_inner = None
                        best_task_num_t26_t27_inner = -1
                        best_sort_key_t26_t27_inner = (
                            float("inf"),
                            (float("inf"), datetime.max),
                            float("inf"),
                        )

                        for task_num, task_deque in active_tasks_t26_t27.items():
                            if not task_deque:
                                continue
                            candidate = task_deque[0]
                            candidate_hours = get_webinar_hours(candidate)

                            if candidate.id in assigned_webinar_ids:
                                task_deque.popleft()
                                candidate_search_restart_needed_t26_t27 = True
                                best_candidate_t26_t27_inner = None
                                break

                            is_t26 = task_num == 26
                            is_t27 = task_num == 27

                            if (
                                hours_filled_this_week + candidate_hours
                                > hours_per_week
                            ):
                                continue
                            if (
                                is_t26
                                and quota_t26 <= 0
                                and current_t26_hours_this_week + candidate_hours
                                > strict_max_t26_hours
                            ):
                                continue
                            if (
                                is_t27
                                and quota_t27 <= 0
                                and current_t27_hours_this_week + candidate_hours
                                > strict_max_t27_hours
                            ):
                                continue
                            # --- ИЗМЕНЕНО: Проверяем недельные квоты вместо общих ---
                            if is_t26 and quota_t26 > 0:
                                # Считаем текущее количество T26 вебинаров на этой неделе
                                week_t26_count = sum(
                                    1
                                    for wid, wk in webinar_weeks.items()
                                    if wk == week_num
                                    and any(
                                        26 in w.task_numbers_set
                                        for w in selected_regular_webinars
                                        if w.id == wid
                                    )
                                )
                                if week_t26_count >= quota_t26:
                                    continue

                            if is_t27 and quota_t27 > 0:
                                # Считаем текущее количество T27 вебинаров на этой неделе
                                week_t27_count = sum(
                                    1
                                    for wid, wk in webinar_weeks.items()
                                    if wk == week_num
                                    and any(
                                        27 in w.task_numbers_set
                                        for w in selected_regular_webinars
                                        if w.id == wid
                                    )
                                )
                                if week_t27_count >= quota_t27:
                                    continue
                            # --- КОНЕЦ ИЗМЕНЕНИЯ ---

                            candidate_sort_key = create_webinar_sort_key(candidate)
                            if candidate_sort_key < best_sort_key_t26_t27_inner:
                                best_candidate_t26_t27_inner = candidate
                                best_task_num_t26_t27_inner = task_num
                                best_sort_key_t26_t27_inner = candidate_sort_key

                        if candidate_search_restart_needed_t26_t27:
                            candidate_search_restart_needed_t26_t27 = False
                            active_tasks_t26_t27 = {
                                k: v for k, v in active_tasks_t26_t27.items() if v
                            }
                            if not active_tasks_t26_t27:
                                break
                            continue
                        else:
                            best_candidate_t26_t27 = best_candidate_t26_t27_inner
                            best_task_num_t26_t27 = best_task_num_t26_t27_inner
                            best_sort_key_t26_t27 = best_sort_key_t26_t27_inner
                            break

                # --- Шаг 3.4: Добавление лучшего кандидата T26/T27, если найден и подходит ---
                if best_candidate_t26_t27:
                    candidate_hours = get_webinar_hours(best_candidate_t26_t27)
                    # Проверки бюджета/капов/квот уже были сделаны при поиске, можно добавлять
                    webinar_to_add = task_deques[best_task_num_t26_t27].popleft()
                    if webinar_to_add.id not in assigned_webinar_ids:
                        w_hours = candidate_hours
                        webinar_weeks[webinar_to_add.id] = week_num
                        selected_regular_webinars.append(webinar_to_add)
                        assigned_webinar_ids.add(webinar_to_add.id)
                        hours_filled_this_week += w_hours
                        added_in_this_iteration = True

                        if best_task_num_t26_t27 == 26:
                            current_t26_hours_this_week += w_hours
                            total_t26_added += 1
                            print(
                                f"    + Added Other (T26) ID: {webinar_to_add.id} ({w_hours:.1f}h). Week total: {hours_filled_this_week:.1f}h. Wk T26: {current_t26_hours_this_week:.1f}h."
                            )
                        elif best_task_num_t26_t27 == 27:
                            current_t27_hours_this_week += w_hours
                            total_t27_added += 1
                            print(
                                f"    + Added Other (T27) ID: {webinar_to_add.id} ({w_hours:.1f}h). Week total: {hours_filled_this_week:.1f}h. Wk T27: {current_t27_hours_this_week:.1f}h."
                            )
                        # --- Переходим к следующей итерации основного цикла while ---
                        continue
                    else:
                        print(
                            f"!!! WARNING: Trying to re-add webinar {webinar_to_add.id} (T26/T27) in Phase 3, skipping."
                        )
                        # added_in_this_iteration остается False, выйдем из цикла

            # --- Шаг 3.5: Если ничего не добавили ни из 1-25, ни из T26/T27, выходим ---
            if not added_in_this_iteration:
                print(
                    "    -> No suitable candidate found in Phase 3 this iteration (from 1-25 or T26/T27)."
                )
                break  # Не нашли подходящего кандидата нигде, завершаем неделю

            # --- Конец основного цикла while для Фазы 3 ---

        weekly_hours_summary[week_num] = hours_filled_this_week
        if not any(task_deques.values()):
            print("\n--- Все очереди задач исчерпаны, завершаем распределение ---")
            break  # Все задачи обработаны

    return webinar_weeks, selected_regular_webinars


# --- Основная функция (рефакторинг) ---


def recommend_webinars(
    student,
    known_task_numbers,
    watched_webinar_ids,
    is_first_plan=True,
    last_plan_completion_perc=0.0,  # Параметр пока не используется, но оставлен
    quota_t26=0,
    quota_t27=0,
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
    all_webinars = Webinar.query.options(db.joinedload(Webinar.task_numbers)).all()
    print(f"Total webinars in DB: {len(all_webinars)}")

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
