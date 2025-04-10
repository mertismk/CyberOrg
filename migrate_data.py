# migrate_data.py
import sqlite3
import os
from datetime import datetime

# --- КОНФИГУРАЦИЯ ---
# SOURCE_DB_PATH = os.path.join('instance', 'cyberorg.db') # Старый путь
# DEST_DB_PATH = 'cyberorg.db' # Старый путь
SOURCE_DB_PATH = os.path.join('test', 'cyberorg.db')   # Новый источник
DEST_DB_PATH = os.path.join('instance', 'cyberorg.db') # Новая цель
# --------------------

TABLES_TO_MIGRATE = [
    {
        'name': 'user',
        'columns': ['id', 'username', 'password_hash', 'role', 'first_name', 'last_name', 'last_login'],
        'pk': 'id',
        'unique_constraints': ['username'] # Дополнительные уникальные поля
    },
    {
        'name': 'student',
        'columns': ['id', 'first_name', 'last_name', 'platform_id', 'registration_date', 'target_score', 'hours_per_week', 'last_plan_id', 'notes', 'is_active', 'initial_score', 'needs_python_basics', 'task_26_deferred', 'task_27_deferred'],
        'pk': 'id',
        'foreign_keys': {'last_plan_id': 'study_plan'} # Указываем внешние ключи для проверки
    },
    {
        'name': 'study_plan',
        'columns': ['id', 'student_id', 'created_at', 'created_by_id'],
        'pk': 'id',
        'foreign_keys': {'student_id': 'student', 'created_by_id': 'user'}
    },
    {
        'name': 'planned_webinar',
        'columns': ['id', 'study_plan_id', 'webinar_id', 'week_number'],
        'pk': 'id',
        'foreign_keys': {'study_plan_id': 'study_plan', 'webinar_id': 'webinar'} # webinar не переносится!
    },
    {
        'name': 'known_task_number',
        'columns': ['id', 'student_id', 'task_number'],
        'pk': 'id',
        'foreign_keys': {'student_id': 'student'}
    },
    {
        'name': 'watched_webinar',
        'columns': ['id', 'student_id', 'webinar_id', 'watched_at', 'created_by_id'],
        'pk': 'id',
        'foreign_keys': {'student_id': 'student', 'webinar_id': 'webinar', 'created_by_id': 'user'} # webinar и user должны существовать в цели!
    }
]

def get_existing_ids(cursor, table_name, column_name='id'):
    """Получает множество существующих ID или значений уникального поля из таблицы."""
    try:
        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        return {row[0] for row in cursor.fetchall() if row[0] is not None}
    except sqlite3.OperationalError as e:
        print(f"Предупреждение: Не удалось получить ID из таблицы {table_name} (возможно, ее нет): {e}")
        return set()

def migrate_table(source_cur, dest_con, dest_cur, table_info):
    """Переносит данные для одной таблицы."""
    table_name = table_info['name']
    columns = table_info['columns']
    pk = table_info['pk']
    unique_constraints = table_info.get('unique_constraints', [])
    foreign_keys = table_info.get('foreign_keys', {})

    print(f"\n--- Перенос таблицы: {table_name} ---")

    # Получаем существующие ID и уникальные значения из целевой базы
    existing_pks = get_existing_ids(dest_cur, table_name, pk)
    existing_uniques = {}
    for u_col in unique_constraints:
        existing_uniques[u_col] = get_existing_ids(dest_cur, table_name, u_col)

    # Получаем существующие ID родительских таблиц для проверки внешних ключей
    existing_fk_ids = {}
    for fk_col, parent_table in foreign_keys.items():
         # Для webinar используем заглушку, т.к. не переносим, но FK есть
        if parent_table == 'webinar':
             print(f"Предупреждение: Проверка FK для {table_name}.{fk_col} на таблицу webinar будет пропущена (предполагаем, что вебинары существуют).")
             existing_fk_ids[fk_col] = None # Сигнал для пропуска проверки
        else:
            existing_fk_ids[fk_col] = get_existing_ids(dest_cur, parent_table, 'id')


    # Получаем данные из исходной базы
    try:
        cols_str = ', '.join(columns)
        source_cur.execute(f"SELECT {cols_str} FROM {table_name}")
        source_data = source_cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Ошибка: Не удалось прочитать таблицу {table_name} из исходной БД: {e}")
        return 0, 0, 0

    inserted_count = 0
    skipped_count = 0
    error_count = 0

    col_placeholders = ', '.join(['?'] * len(columns))
    sql = f"INSERT OR IGNORE INTO {table_name} ({cols_str}) VALUES ({col_placeholders})"

    for row_tuple in source_data:
        row = dict(zip(columns, row_tuple))
        pk_value = row[pk]

        # 1. Проверка первичного ключа
        if pk_value in existing_pks:
            # print(f"Пропуск {table_name}: Запись с ID {pk_value} уже существует.")
            skipped_count += 1
            continue

        # 2. Проверка уникальных ключей
        skipped_due_to_unique = False
        for u_col in unique_constraints:
            if row.get(u_col) in existing_uniques[u_col]:
                # print(f"Пропуск {table_name}: Запись с {u_col} = {row.get(u_col)} уже существует.")
                skipped_count += 1
                skipped_due_to_unique = True
                break
        if skipped_due_to_unique:
            continue

        # 3. Проверка внешних ключей (если значение не NULL)
        fk_violation = False
        for fk_col, parent_ids_set in existing_fk_ids.items():
            fk_value = row.get(fk_col)
            # Пропускаем проверку для NULL значений или если parent_ids_set is None (случай с webinar)
            if fk_value is not None and parent_ids_set is not None:
                if fk_value not in parent_ids_set:
                    print(f"Ошибка FK {table_name}: Запись ID={pk_value} ссылается на несуществующий {fk_col}={fk_value}.")
                    error_count += 1
                    fk_violation = True
                    break # Достаточно одной ошибки FK
        if fk_violation:
            continue

        # 4. Вставка данных
        try:
            # Преобразуем datetime в строку ISO для SQLite, если необходимо
            values_to_insert = []
            for col_name in columns:
                value = row[col_name]
                if isinstance(value, datetime):
                     # SQLite обычно хранит datetime как TEXT в ISO формате или REAL/INTEGER timestamp
                     # Используем ISO формат для совместимости
                     values_to_insert.append(value.isoformat())
                else:
                     values_to_insert.append(value)

            dest_cur.execute(sql, tuple(values_to_insert))
            if dest_cur.rowcount > 0:
                inserted_count += 1
                # Добавляем только что вставленные ID в множества для проверки последующих строк
                existing_pks.add(pk_value)
                for u_col in unique_constraints:
                    if row.get(u_col) is not None:
                        existing_uniques[u_col].add(row.get(u_col))
            else:
                # Если rowcount == 0 после INSERT OR IGNORE, значит запись уже была (хотя мы проверяли)
                # Это может случиться в редких случаях или если проверка была неполной
                 skipped_count += 1

        except sqlite3.IntegrityError as e:
            print(f"Ошибка целостности при вставке {table_name} ID={pk_value}: {e}")
            error_count += 1
        except Exception as e:
            print(f"Неизвестная ошибка при вставке {table_name} ID={pk_value}: {e}")
            error_count += 1


    dest_con.commit()
    print(f"Таблица {table_name}: Вставлено = {inserted_count}, Пропущено (дубликаты) = {skipped_count}, Ошибки = {error_count}")
    return inserted_count, skipped_count, error_count

def main():
    print("Начало миграции данных...")
    print(f"Источник: {SOURCE_DB_PATH}")
    print(f"Назначение: {DEST_DB_PATH}")

    if not os.path.exists(SOURCE_DB_PATH):
        print(f"Ошибка: Исходная база данных не найдена: {SOURCE_DB_PATH}")
        return

    if not os.path.exists(DEST_DB_PATH):
        print(f"Ошибка: Целевая база данных не найдена: {DEST_DB_PATH}")
        print("Пожалуйста, убедитесь, что файл cyberorg.db существует (возможно, нужно запустить приложение для его создания).")
        return

    # Подключение к базам данных
    try:
        source_conn = sqlite3.connect(SOURCE_DB_PATH)
        # Для правильной обработки datetime из строк
        dest_conn = sqlite3.connect(DEST_DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        # Используем Row factory для доступа к данным по имени колонки
        source_conn.row_factory = sqlite3.Row
        dest_conn.row_factory = sqlite3.Row

        source_cur = source_conn.cursor()
        dest_cur = dest_conn.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базам данных: {e}")
        return

    total_inserted = 0
    total_skipped = 0
    total_errors = 0

    # Перенос таблиц в определенном порядке
    for table_info in TABLES_TO_MIGRATE:
        inserted, skipped, errors = migrate_table(source_cur, dest_conn, dest_cur, table_info)
        total_inserted += inserted
        total_skipped += skipped
        total_errors += errors

    # Закрытие соединений
    source_conn.close()
    dest_conn.close()

    print("\n--- Миграция завершена ---")
    print(f"Всего вставлено записей: {total_inserted}")
    print(f"Всего пропущено записей (дубликаты): {total_skipped}")
    print(f"Всего ошибок при вставке: {total_errors}")

if __name__ == "__main__":
    print("ВАЖНО: Перед запуском убедитесь, что вы сделали резервную копию файла cyberorg.db!")
    confirm = input("Продолжить миграцию? (yes/no): ")
    if confirm.lower() == 'yes':
        main()
    else:
        print("Миграция отменена.")
