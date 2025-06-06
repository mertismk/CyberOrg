# CyberOrg - Система планирования обучения

CyberOrg - это веб-приложение для планирования и организации обучения учеников. Система помогает кураторам эффективно составлять индивидуальные планы обучения, отслеживать прогресс и оптимизировать учебный процесс.

## Основные возможности

- Управление учениками и их профилями
- Создание индивидуальных планов обучения
- Отслеживание прогресса по просмотренным вебинарам
- Управление базой вебинаров
- Импорт вебинаров из Excel-файлов
- Автоматический подбор вебинаров на основе уровня и целей ученика

## Установка и запуск

### Предварительные требования

- Python 3.9+
- PostgreSQL или SQLite
- pip (менеджер пакетов Python)

### Шаги установки

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/CyberOrg.git
   cd CyberOrg
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # для Linux/Mac
   # или
   .venv\Scripts\activate     # для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте переменные окружения (по желанию, создайте файл `.env`):
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///instance/cyberorg.db
   # или для PostgreSQL
   # DATABASE_URL=postgresql://username:password@localhost/cyberorg
   SECRET_KEY=ваш_секретный_ключ
   ```

5. Инициализируйте базу данных:
   ```bash
   flask init-db
   ```

6. Запустите приложение:
   ```bash
   flask run
   ```
   или
   ```bash
   python run.py
   ```

## Развертывание на сервере

Для продакшн-развертывания рекомендуется использовать Gunicorn и Nginx:

1. Установите Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Создайте systemd-сервис:
   ```
   [Unit]
   Description=Gunicorn instance to serve CyberOrg
   After=network.target

   [Service]
   User=your_username
   Group=www-data
   WorkingDirectory=/path/to/CyberOrg
   Environment="PATH=/path/to/CyberOrg/.venv/bin"
   ExecStart=/path/to/CyberOrg/.venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"

   [Install]
   WantedBy=multi-user.target
   ```

3. Настройте Nginx как обратный прокси-сервер

## Структура проекта

- `run.py` - точка входа приложения
- `config.py` - конфигурация приложения
- `app/` - основной пакет приложения
  - `__init__.py` - инициализация приложения и подключение blueprints
  - `models.py` - модели данных
  - `templates/` - HTML-шаблоны
  - `static/` - статические файлы (CSS, JavaScript)
  - Blueprints:
    - `auth/` - аутентификация и авторизация
    - `main/` - основные маршруты
    - `users/` - управление пользователями
    - `students/` - управление учениками
    - `webinars/` - управление вебинарами
    - `plans/` - управление планами обучения

## Роли пользователей

- **Куратор (regular)**: Базовая роль для работы с учениками и планами
- **Администратор (admin)**: Доступ к импорту вебинаров и расширенному функционалу
- **Супер-администратор (super_admin)**: Полный доступ, включая управление пользователями

## Контакты

По вопросам и предложениям обращайтесь по адресу: mkmertis@gmail.com
