"""
Сервис для создания параллельных ОГЭ планов.

Система работает с параллельным изучением тем в определенном порядке:
1. Системы счисления
2. Программирование  
3. Графы
4. Кодирование

Может быть максимум 2 темы параллельно (1-2 вебинара в неделю).
Когда тема заканчивается, она заменяется на следующую из очереди.
"""

from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

from app import db
from app.models import (
    OGETopic, OGETopicOrder, OGEParallelPlan, OGEParallelPlanSlot, 
    OGEParallelPlanWebinar, OGEParallelPlanTopicOrder, Webinar, Student, WatchedWebinar
)


def initialize_oge_topic_order():
    """
    Инициализирует порядок изучения тем ОГЭ с приоритетами.
    Вызывается один раз для настройки системы.
    """
    # Проверяем, есть ли уже записи
    if OGETopicOrder.query.first():
        print("Порядок тем ОГЭ уже инициализирован")
        return
    
    # Определяем порядок тем ОГЭ с номерами заданий и приоритетами
    topic_order = [
        ("Системы счисления", "10", 1),  # Приоритет 1
        ("Программирование", "6", 2),    # Приоритет 2
        ("Графы", "4, 9", 3),           # Приоритет 3
        ("Кодирование информации", "1, 2", 4),  # Приоритет 4
        ("Алгебра логики", "3, 8", None),       # Без приоритета
        ("Алгоритмы и исполнители", "5, 15", None),  # Без приоритета
        ("Электронные таблицы и текстовый редактор", "7, 13, 14", None),  # Без приоритета
        ("Файловая система", "11, 12", None)  # Без приоритета
    ]
    
    for order_index, (topic_name, task_numbers, priority) in enumerate(topic_order):
        # Ищем тему по имени
        topic = OGETopic.query.filter_by(name=topic_name, is_active=True).first()
        if topic:
            # Обновляем номера заданий если они не заданы
            if not topic.task_numbers_str:
                topic.task_numbers_str = task_numbers
                print(f"Обновлены номера заданий для темы '{topic_name}': {task_numbers}")
            
            # Устанавливаем приоритет если он задан
            if priority is not None:
                topic.priority = priority
                print(f"Установлен приоритет {priority} для темы '{topic_name}'")
            
            topic_order_entry = OGETopicOrder(
                topic_id=topic.id,
                order_index=order_index,
                is_active=True
            )
            db.session.add(topic_order_entry)
            print(f"Добавлена тема '{topic_name}' с порядком {order_index}")
        else:
            print(f"ВНИМАНИЕ: Тема '{topic_name}' не найдена в базе данных")
    
    try:
        db.session.commit()
        print("Порядок тем ОГЭ успешно инициализирован")
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка инициализации порядка тем ОГЭ: {e}")
        raise


def get_oge_topics_in_order(plan: Optional[OGEParallelPlan] = None) -> List[OGETopic]:
    """Возвращает темы ОГЭ в порядке: кастомный для плана, иначе глобальный."""
    if plan is not None:
        # Пробуем взять кастомный порядок для плана
        custom = (db.session.query(OGETopic)
                  .join(OGEParallelPlanTopicOrder, OGETopic.id == OGEParallelPlanTopicOrder.topic_id)
                  .filter(OGEParallelPlanTopicOrder.plan_id == plan.id, OGETopic.is_active == True)
                  .order_by(OGEParallelPlanTopicOrder.order_index)
                  .all())
        if custom:
            return custom
    # Фоллбек: глобальный порядок
    return (db.session.query(OGETopic)
            .join(OGETopicOrder, OGETopic.id == OGETopicOrder.topic_id)
            .filter(OGETopic.is_active == True, OGETopicOrder.is_active == True)
            .order_by(OGETopicOrder.order_index)
            .all())


def get_topic_emoji(topic_name: str) -> str:
    """Возвращает эмодзи для темы ОГЭ"""
    emoji_map = {
        'Системы счисления': '🔢',
        'Графы': '🕸️',
        'Кодирование информации': '📡',
        'Алгебра логики': '⚙️',
        'Алгоритмы и исполнители': '🤖',
        'Программирование': '💻',
        'Электронные таблицы и текстовый редактор': '📊',
        'Файловая система': '📂',
    }
    return emoji_map.get(topic_name, '📚')


def get_hard_prog_webinars(student: Student) -> List[Webinar]:
    """Возвращает вебинары хард-вебинаров ОГЭ для студента"""
    # Получаем просмотренные вебинары студента
    watched_webinar_ids = {
        w.webinar_id for w in WatchedWebinar.query.filter_by(student_id=student.id).all()
    }
    
    # Получаем вебинары хард-проги (ОГЭ, активные, не просмотренные, с реальными данными)
    webinars = (db.session.query(Webinar)
                .filter(
                    Webinar.exam_type == 'oge',
                    Webinar.academic_year == student.academic_year,
                    Webinar.for_oge_hard == True,  # Хард-вебинары ОГЭ
                    Webinar.title.isnot(None),  # Только вебинары с названием
                    Webinar.title != '',  # Не пустые названия
                    ~Webinar.id.in_(watched_webinar_ids) if watched_webinar_ids else True
                )
                .order_by(Webinar.date.asc().nullslast(), Webinar.id.asc())
                .all())
    
    return webinars


def get_webinars_for_topic(topic: OGETopic, student: Student) -> List[Webinar]:
    """
    Возвращает вебинары для темы, отфильтрованные и отсортированные для студента
    """
    # Получаем просмотренные вебинары студента
    watched_webinar_ids = {
        w.webinar_id for w in WatchedWebinar.query.filter_by(student_id=student.id).all()
    }
    
    # Получаем вебинары для темы (ОГЭ, активные, не просмотренные, с реальными данными)
    webinars = (db.session.query(Webinar)
                .join(Webinar.oge_topics)
                .filter(
                    OGETopic.id == topic.id,
                    Webinar.exam_type == 'oge',
                    Webinar.academic_year == student.academic_year,
                    Webinar.title.isnot(None),  # Только вебинары с названием
                    Webinar.title != '',  # Не пустые названия
                    ~Webinar.id.in_(watched_webinar_ids) if watched_webinar_ids else True
                )
                .order_by(Webinar.date.asc().nullslast(), Webinar.id.asc())
                .all())
    
    return webinars


def create_oge_parallel_plan(student: Student, webinars_per_week: int, hard_prog_webinars_per_week: int = 0, created_by_id: int = None) -> OGEParallelPlan:
    """
    Создает параллельный план изучения ОГЭ для студента.
    
    Args:
        student: Студент для которого создается план
        webinars_per_week: Количество обычных вебинаров в неделю (1-3)
        hard_prog_webinars_per_week: Количество вебинаров хард-вебинаров ОГЭ в неделю (0-1)
        created_by_id: ID пользователя создающего план
    
    Returns:
        OGEParallelPlan: Созданный план
    """
    if webinars_per_week < 1 or webinars_per_week > 3:
        raise ValueError("Количество обычных вебинаров в неделю должно быть от 1 до 3")
    if hard_prog_webinars_per_week < 0 or hard_prog_webinars_per_week > 1:
        raise ValueError("Количество вебинаров хард-вебинаров ОГЭ в неделю должно быть 0 или 1")
    if webinars_per_week + hard_prog_webinars_per_week > 3:
        raise ValueError("Всего вебинаров в неделю не может быть больше 3")
    if student.exam_type != 'oge':
        raise ValueError("План может быть создан только для студентов ОГЭ")

    # Создаем план
    plan = OGEParallelPlan(
        student_id=student.id,
        webinars_per_week=webinars_per_week,
        hard_prog_webinars_per_week=hard_prog_webinars_per_week,
        created_by_id=created_by_id,
        is_active=True
    )
    db.session.add(plan)
    db.session.flush()  # Чтобы получить ID плана

    # Создаем обычные слоты (1, 2 или 3)
    for slot_num in range(1, webinars_per_week + 1):
        slot = OGEParallelPlanSlot(
            plan_id=plan.id,
            slot_number=slot_num,
            current_topic_id=None,
            current_topic_position=0,
            is_completed=False
        )
        db.session.add(slot)

    # Заполняем план вебинарами
    weeks_to_fill = 4  # По умолчанию заполняем на 4 недели
    _fill_parallel_plan(plan, weeks_to_fill)

    # Если включены хард-вебинары ОГЭ, добавляем их (отдельный слот 0)
    if plan.hard_prog_webinars_per_week > 0:
        _add_hard_prog_webinars(plan, weeks_to_fill)

    db.session.commit()
    return plan


def _fill_parallel_plan(plan: OGEParallelPlan, weeks_to_fill: int = 4):
    """
    Заполняет параллельный план вебинарами на указанное количество недель.
    
    Args:
        plan: План для заполнения
        weeks_to_fill: Количество недель для заполнения (по умолчанию 4)
    """
    topics_in_order = get_oge_topics_in_order(plan)
    if not topics_in_order:
        raise ValueError("Не найдены темы ОГЭ в правильном порядке")
    
    # Сортируем темы по приоритету (сначала с приоритетом, потом без)
    topics_with_priority = [t for t in topics_in_order if t.priority is not None]
    topics_without_priority = [t for t in topics_in_order if t.priority is None]
    
    # Сортируем темы с приоритетом по приоритету (1-4)
    topics_with_priority.sort(key=lambda x: x.priority)
    
    # Объединяем: сначала с приоритетом, потом без
    sorted_topics = topics_with_priority + topics_without_priority
    
    # Инициализируем слоты первыми темами
    slots = plan.slots
    for i, slot in enumerate(slots):
        if i < len(sorted_topics):
            slot.current_topic_id = sorted_topics[i].id
            slot.current_topic_position = 0
            slot.is_completed = False
    
    # Создаем словарь для отслеживания позиций в темах по слотам
    topic_positions = {slot.slot_number: 0 for slot in slots}
    
    # Заполняем план по неделям
    for week in range(1, weeks_to_fill + 1):
        week_webinars_added = 0
        
        # Проходим по слотам в каждой неделе
        for slot in slots:
            current_topic = slot.current_topic
            if not current_topic or slot.is_completed:
                continue
            
            # Проверяем, не превысили ли лимит вебинаров в неделю
            if week_webinars_added >= plan.webinars_per_week:
                break
            
            # Получаем вебинары для текущей темы слота
            topic_webinars = get_webinars_for_topic(current_topic, plan.student)
            
            # Проверяем, есть ли еще вебинары в этой теме
            if topic_positions[slot.slot_number] >= len(topic_webinars):
                # Тема закончилась, переходим к следующей
                next_topic = _get_next_topic_for_slot(slot, topics_in_order)
                if next_topic:
                    slot.current_topic_id = next_topic.id
                    slot.current_topic_position = 0
                    slot.is_completed = False
                    topic_positions[slot.slot_number] = 0
                    topic_webinars = get_webinars_for_topic(next_topic, plan.student)
                    current_topic = next_topic  # Обновляем текущую тему
                else:
                    # Больше нет тем для изучения
                    slot.is_completed = True
                    continue
            
            # Если есть вебинары, добавляем следующий
            if topic_positions[slot.slot_number] < len(topic_webinars):
                webinar = topic_webinars[topic_positions[slot.slot_number]]
                
                # Проверяем, что вебинар еще не добавлен в план
                existing = (db.session.query(OGEParallelPlanWebinar)
                           .filter_by(plan_id=plan.id, webinar_id=webinar.id)
                           .first())
                
                if not existing:
                    plan_webinar = OGEParallelPlanWebinar(
                        plan_id=plan.id,
                        webinar_id=webinar.id,
                        slot_number=slot.slot_number,
                        week_number=week,
                        topic_id=current_topic.id,
                        position_in_topic=topic_positions[slot.slot_number]
                    )
                    db.session.add(plan_webinar)
                    week_webinars_added += 1
                
                # Увеличиваем позицию в теме
                topic_positions[slot.slot_number] += 1
                slot.current_topic_position = topic_positions[slot.slot_number]


def _get_next_topic_for_slot(slot: OGEParallelPlanSlot, topics_in_order: List[OGETopic]) -> Optional[OGETopic]:
    """
    Определяет следующую тему для слота после завершения текущей.
    Учитывает приоритеты тем.
    
    Args:
        slot: Слот плана
        topics_in_order: Темы в правильном порядке
    
    Returns:
        OGETopic: Следующая тема или None если тем больше нет
    """
    current_topic = slot.current_topic
    if not current_topic:
        return topics_in_order[0] if topics_in_order else None
    
    # Сортируем темы по приоритету
    topics_with_priority = [t for t in topics_in_order if t.priority is not None]
    topics_without_priority = [t for t in topics_in_order if t.priority is None]
    topics_with_priority.sort(key=lambda x: x.priority)
    sorted_topics = topics_with_priority + topics_without_priority
    
    # Находим текущую тему в отсортированном списке
    current_order = None
    for i, topic in enumerate(sorted_topics):
        if topic.id == current_topic.id:
            current_order = i
            break
    
    if current_order is None:
        return sorted_topics[0] if sorted_topics else None
    
    # Ищем следующую тему, которая еще не используется в других слотах плана
    plan = slot.plan
    used_topic_ids = {s.current_topic_id for s in plan.slots if s.slot_number != slot.slot_number and not s.is_completed}
    
    for i in range(current_order + 1, len(sorted_topics)):
        if sorted_topics[i].id not in used_topic_ids:
            return sorted_topics[i]
    
    # Если не найдено уникальных тем, возвращаем следующую по порядку
    if current_order + 1 < len(sorted_topics):
        return sorted_topics[current_order + 1]
    
    return None


def get_plan_progress(plan: OGEParallelPlan) -> Dict:
    """
    Возвращает информацию о прогрессе выполнения плана.
    
    Returns:
        dict: Словарь с информацией о прогрессе
    """
    # Получаем просмотренные вебинары студента
    watched_webinar_ids = {
        w.webinar_id for w in WatchedWebinar.query.filter_by(student_id=plan.student_id).all()
    }
    
    # Общая статистика
    total_webinars = len(plan.webinars)
    watched_count = sum(1 for pw in plan.webinars if pw.webinar_id in watched_webinar_ids)
    
    # Статистика по темам
    topic_progress = defaultdict(lambda: {'total': 0, 'watched': 0, 'progress': 0, 'emoji': '', 'task_numbers_str': ''})
    
    for plan_webinar in plan.webinars:
        if plan_webinar.topic:  # Проверяем, что тема существует
            topic_name = plan_webinar.topic.name
            topic_progress[topic_name]['total'] += 1
            topic_progress[topic_name]['emoji'] = get_topic_emoji(topic_name)
            topic_progress[topic_name]['task_numbers_str'] = plan_webinar.topic.task_numbers_str or ''
            if plan_webinar.webinar_id in watched_webinar_ids:
                topic_progress[topic_name]['watched'] += 1
    
    # Вычисляем процент прогресса по темам
    for topic_name, stats in topic_progress.items():
        if stats['total'] > 0:
            stats['progress'] = round((stats['watched'] / stats['total']) * 100, 1)
    
    # Статистика по неделям
    weekly_progress = defaultdict(lambda: {'total': 0, 'watched': 0, 'progress': 0})
    
    for plan_webinar in plan.webinars:
        week = plan_webinar.week_number
        weekly_progress[week]['total'] += 1
        if plan_webinar.webinar_id in watched_webinar_ids:
            weekly_progress[week]['watched'] += 1
    
    # Вычисляем процент прогресса по неделям
    for week, stats in weekly_progress.items():
        if stats['total'] > 0:
            stats['progress'] = round((stats['watched'] / stats['total']) * 100, 1)
    
    return {
        'total_webinars': total_webinars,
        'watched_count': watched_count,
        'overall_progress': round((watched_count / total_webinars) * 100, 1) if total_webinars > 0 else 0,
        'topic_progress': dict(topic_progress),
        'weekly_progress': dict(weekly_progress)
    }


def extend_parallel_plan(plan: OGEParallelPlan, additional_weeks: int = 4):
    """
    Расширяет существующий план на дополнительные недели.
    
    Args:
        plan: Существующий план для расширения
        additional_weeks: Количество дополнительных недель
    """
    # Находим максимальную неделю в текущем плане
    max_week = max((pw.week_number for pw in plan.webinars), default=0)
    
    # Временно сохраняем текущие позиции слотов
    current_positions = {}
    for slot in plan.slots:
        current_positions[slot.slot_number] = slot.current_topic_position
    
    # Продолжаем заполнение с следующей недели
    _fill_parallel_plan_from_week(plan, max_week + 1, additional_weeks, current_positions)
    
    db.session.commit()


def _fill_parallel_plan_from_week(plan: OGEParallelPlan, start_week: int, weeks_count: int, topic_positions: Dict[int, int]):
    """
    Заполняет план начиная с определенной недели.
    
    Args:
        plan: План для заполнения
        start_week: Начальная неделя
        weeks_count: Количество недель для заполнения
        topic_positions: Текущие позиции в темах по слотам
    """
    topics_in_order = get_oge_topics_in_order(plan)
    
    for week in range(start_week, start_week + weeks_count):
        week_webinars_added = 0
        
        for slot in plan.slots:
            current_topic = slot.current_topic
            if not current_topic or slot.is_completed:
                continue
            
            # Проверяем, не превысили ли лимит вебинаров в неделю
            if week_webinars_added >= plan.webinars_per_week:
                break
            
            topic_webinars = get_webinars_for_topic(current_topic, plan.student)
            
            # Проверяем, есть ли еще вебинары в этой теме
            if topic_positions[slot.slot_number] >= len(topic_webinars):
                # Тема закончилась, переходим к следующей
                next_topic = _get_next_topic_for_slot(slot, topics_in_order)
                if next_topic:
                    slot.current_topic_id = next_topic.id
                    slot.current_topic_position = 0
                    slot.is_completed = False
                    topic_positions[slot.slot_number] = 0
                    topic_webinars = get_webinars_for_topic(next_topic, plan.student)
                    current_topic = next_topic
                else:
                    slot.is_completed = True
                    continue
            
            if topic_positions[slot.slot_number] < len(topic_webinars):
                webinar = topic_webinars[topic_positions[slot.slot_number]]
                
                existing = (db.session.query(OGEParallelPlanWebinar)
                           .filter_by(plan_id=plan.id, webinar_id=webinar.id)
                           .first())
                
                if not existing:
                    plan_webinar = OGEParallelPlanWebinar(
                        plan_id=plan.id,
                        webinar_id=webinar.id,
                        slot_number=slot.slot_number,
                        week_number=week,
                        topic_id=current_topic.id,
                        position_in_topic=topic_positions[slot.slot_number]
                    )
                    db.session.add(plan_webinar)
                    week_webinars_added += 1
                
                topic_positions[slot.slot_number] += 1
                slot.current_topic_position = topic_positions[slot.slot_number]


def get_parallel_plan_visual_data(plan: OGEParallelPlan) -> Dict:
    """
    Возвращает данные для визуализации параллельного плана.
    
    Returns:
        dict: Данные для отображения плана
    """
    # Получаем просмотренные вебинары
    watched_webinar_ids = {
        w.webinar_id for w in WatchedWebinar.query.filter_by(student_id=plan.student_id).all()
    }
    
    # Группируем вебинары по неделям и слотам
    weeks_data = defaultdict(lambda: defaultdict(list))
    
    for plan_webinar in plan.webinars:
        week = plan_webinar.week_number
        slot = plan_webinar.slot_number
        
        webinar_data = {
            'webinar': plan_webinar.webinar,
            'topic': plan_webinar.topic,
            'position_in_topic': plan_webinar.position_in_topic,
            'is_watched': plan_webinar.webinar_id in watched_webinar_ids,
            'plan_webinar': plan_webinar
        }
        
        weeks_data[week][slot].append(webinar_data)
    
    # Сортируем по неделям
    sorted_weeks = {}
    for week in sorted(weeks_data.keys()):
        sorted_weeks[week] = dict(weeks_data[week])
        # Сортируем вебинары в каждом слоте по позиции в теме
        for slot in sorted_weeks[week]:
            sorted_weeks[week][slot].sort(key=lambda x: x['position_in_topic'])
    
    return {
        'weeks_data': sorted_weeks,
        'plan': plan,
        'progress': get_plan_progress(plan)
    }


def _add_hard_prog_webinars(plan: OGEParallelPlan, weeks_to_fill: int):
    """Добавляет вебинары хард-вебинаров ОГЭ в план (максимум 1 в неделю)"""
    if plan.hard_prog_webinars_per_week == 0:
        return
    
    hard_prog_webinars = get_hard_prog_webinars(plan.student)
    if not hard_prog_webinars:
        return
    
    webinar_index = 0
    
    for week in range(1, weeks_to_fill + 1):
        # Добавляем только 1 вебинар хард-вебинаров ОГЭ в неделю
        if webinar_index < len(hard_prog_webinars):
            webinar = hard_prog_webinars[webinar_index]
            
            # Проверяем, что вебинар еще не добавлен в план
            existing = (db.session.query(OGEParallelPlanWebinar)
                       .filter_by(plan_id=plan.id, webinar_id=webinar.id)
                       .first())
            
            if not existing:
                # Добавляем вебинар хард-вебинаров ОГЭ в план
                plan_webinar = OGEParallelPlanWebinar(
                    plan_id=plan.id,
                    webinar_id=webinar.id,
                    slot_number=0,  # Специальный слот для хард-вебинаров ОГЭ
                    week_number=week,
                    topic_id=None,  # Хард-вебинары ОГЭ не привязаны к конкретной теме
                    position_in_topic=0
                )
                db.session.add(plan_webinar)
            
            webinar_index += 1
        else:
            break


def generate_student_message(plan: OGEParallelPlan, visual_data: Dict) -> str:
    """
    Генерирует сообщение для отправки ученику с планом вебинаров.
    
    Args:
        plan: План ОГЭ
        visual_data: Данные для визуализации плана
    
    Returns:
        str: Сформированное сообщение для ученика
    """
    # Получаем эмодзи для тем
    topic_emojis = {
        'Системы счисления': '🔢',
        'Графы': '🕸️',
        'Кодирование информации': '📡',
        'Алгебра логики': '⚙️',
        'Алгоритмы и исполнители': '🤖',
        'Программирование': '💻',
        'Электронные таблицы и текстовый редактор': '📊',
        'Файловая система': '📂'
    }
    
    # Начинаем формировать сообщение
    message = "Вот ваш план вебинаров исходя из вашего уровня и желаемого балла.\n\n"
    message += "Цифрами вебинары примерно разделены на недели. После того, как пройдете этот материал, напишите нам для корректировки плана подготовки!\n\n"
    
    # Добавляем вебинары по неделям
    weeks_data = visual_data.get('weeks_data', {})
    for week_num in sorted(weeks_data.keys()):
        message += f"{week_num}️⃣\n\n"
        
        week_data = weeks_data[week_num]
        
        # Собираем все вебинары недели
        week_webinars = []
        for slot_num in sorted(week_data.keys()):
            slot_webinars = week_data[slot_num]
            for webinar_data in slot_webinars:
                webinar = webinar_data['webinar']
                topic = webinar_data.get('topic')
                
                # Определяем эмодзи
                if slot_num == 0:  # Хард-вебинары
                    emoji = "🔥"
                elif topic and topic.name in topic_emojis:
                    emoji = topic_emojis[topic.name]
                else:
                    emoji = "📚"
                
                week_webinars.append(f"{emoji} {webinar.title}\n{webinar.url}")
        
        # Добавляем вебинары недели
        for webinar_text in week_webinars:
            message += webinar_text + "\n\n"
    
    # Добавляем планирование
    message += "📅 Планирование:\n\n"
    message += "Важно распределить время правильно, чтобы охватить все темы. Вы начали готовиться уже сейчас, что похвально! Этого времени хватит на то, чтобы готовиться к информатике без спешки и стресса.\n\n"
    message += "Глобально вам предстоит изучить задания №1–16.\n\n"
    
    # Определяем количество вебинаров
    total_webinars = plan.webinars_per_week
    if plan.hard_prog_webinars_per_week > 0:
        total_webinars += plan.hard_prog_webinars_per_week
    
    message += f"Вам нужно смотреть {total_webinars} вебинара и качественно выполнять домашнее задание к каждому.\n\n"
    message += "Это поможет лучше закрепить материал, так как в первую очередь опыт мы получаем на практике.\n"
    message += "Одному домашнему заданию не стоит уделять более 1,5–2 часов, если решите не всё — не переживайте и помните, что вы всегда можете обратиться за помощью к кураторам в чате!\n"
    message += "Как только обретете небольшую базу, старайтесь писать пробники хотя бы раз в две недели 🧡\n\n"
    
    # Добавляем итоги
    message += "📆 Подытожим ваш план по информатике на неделю:\n"
    message += f"✔️ {plan.webinars_per_week} вебинара\n"
    if plan.hard_prog_webinars_per_week > 0:
        message += "✔️ 1 вебинар по хард-проге\n"
    message += "✔️ домашняя работа к каждому вебинару\n"
    message += "✔️ решать пробники 2 раза в месяц\n\n"
    
    # Добавляем ссылку на таблицу
    message += "📑 При желании можете пользоваться шаблоном нашей таблицы для планирования своей подготовки к ОГЭ: https://docs.google.com/spreadsheets/d/10BHRb5qGx00xk2g634qz2K8Yuh-r4fqKpmgYjcRXauY/edit?usp=sharing\n"
    message += "В ней вы можете отмечать просмотренные вебинары и выполненные домашние задания сразу по нескольким предметам, планировать учебные и не только дела на предстоящий день или неделю.\n"
    message += "Чтобы сохранить шаблон себе, нужно нажать в левом верхнем углу на \"Файл\" ⮕ \"Создать копию\"\n\n"
    
    # Добавляем заключение
    message += "❗️ Если вдруг нагрузка окажется слишком высокой или будут возникать трудности, то напишите повторно.\n\n"
    message += "Прочтите план внимательно. Всё ли вам понятно? Если да, то двигаемся дальше: поговорим немного про структуру экзамена и обсудим навигацию по курсу."
    
    return message
