#!/usr/bin/env python3
"""
Скрипт для исправления порядка тем ОГЭ на продакшн сервере.
Исправляет ошибку "Не найдены темы ОГЭ в правильном порядке"
"""

import sys
import os

# Добавляем путь к приложению
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import OGETopic, OGETopicOrder

def fix_oge_topics():
    """Исправляет порядок тем ОГЭ в базе данных"""
    app = create_app()
    
    with app.app_context():
        print("=== ИСПРАВЛЕНИЕ ПОРЯДКА ТЕМ ОГЭ ===")
        
        # Проверяем текущее состояние
        print("\n1. Проверяем текущее состояние тем ОГЭ...")
        topics = OGETopic.query.filter_by(is_active=True).all()
        print(f"Найдено активных тем: {len(topics)}")
        for topic in topics:
            print(f"  - ID: {topic.id}, Название: {topic.name}, Приоритет: {topic.priority}")
        
        print("\n2. Проверяем текущий порядок тем...")
        orders = OGETopicOrder.query.filter_by(is_active=True).all()
        print(f"Найдено записей в порядке тем: {len(orders)}")
        for order in orders:
            print(f"  - Порядок: {order.order_index}, Тема ID: {order.topic_id}")
        
        # Очищаем старые записи
        print("\n3. Очищаем старые записи порядка тем...")
        OGETopicOrder.query.delete()
        db.session.commit()
        print("Старые записи удалены")
        
        # Создаем правильный порядок тем
        print("\n4. Создаем правильный порядок тем...")
        
        # Определяем правильный порядок тем согласно списку пользователя
        topic_order = [
            ('Системы счисления', 1, 1),  # Приоритет 1
            ('Программирование', 6, 2),    # Приоритет 2  
            ('Графы', 2, 3),              # Приоритет 3
            ('Кодирование информации', 3, 4),  # Приоритет 4
            ('Алгебра логики', 4, None),       # Без приоритета
            ('Алгоритмы и исполнители', 5, None),  # Без приоритета
            ('Электронные таблицы и текстовый редактор', 7, None),  # Без приоритета
            ('Файловая система', 8, None),  # Без приоритета
        ]
        
        for order_index, (topic_name, topic_id, priority) in enumerate(topic_order):
            # Проверяем, что тема существует
            topic = OGETopic.query.get(topic_id)
            if topic:
                # Устанавливаем приоритет если он задан
                if priority is not None:
                    topic.priority = priority
                    print(f"  ✓ Установлен приоритет {priority} для темы '{topic_name}'")
                
                # Создаем запись в порядке тем
                topic_order_entry = OGETopicOrder(
                    topic_id=topic_id,
                    order_index=order_index,
                    is_active=True
                )
                db.session.add(topic_order_entry)
                print(f"  ✓ Добавлена тема '{topic_name}' с порядком {order_index}")
            else:
                print(f"  ✗ ОШИБКА: Тема с ID {topic_id} не найдена!")
        
        # Сохраняем изменения
        try:
            db.session.commit()
            print("\n5. Изменения успешно сохранены в базу данных!")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ ОШИБКА при сохранении: {e}")
            return False
        
        # Проверяем результат
        print("\n6. Проверяем результат...")
        from app.services.oge_plan_service import get_oge_topics_in_order
        topics_in_order = get_oge_topics_in_order()
        print(f"Найдено тем в правильном порядке: {len(topics_in_order)}")
        for topic in topics_in_order:
            print(f"  - {topic.name} (приоритет: {topic.priority})")
        
        if len(topics_in_order) > 0:
            print("\n✅ ПРОБЛЕМА ИСПРАВЛЕНА! Теперь можно создавать планы ОГЭ.")
            return True
        else:
            print("\n❌ ПРОБЛЕМА НЕ РЕШЕНА. Проверьте логи выше.")
            return False

if __name__ == "__main__":
    try:
        success = fix_oge_topics()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        sys.exit(1)
