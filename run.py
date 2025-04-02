from app import create_app, db
from app.models import TaskNumber, User # Добавьте другие модели по мере необходимости

app = create_app()

# Функция для инициализации базы данных
@app.cli.command('init-db')
def init_db_command():
    """Инициализация базы данных начальными данными."""
    # --- Начало изменений: Добавляем создание таблиц --- 
    print("Создание таблиц базы данных...")
    db.create_all()
    print("Таблицы созданы.")
    # --- Конец изменений ---
    # Создаем номера заданий
    print("Добавление номеров заданий...")
    for i in range(1, 28):
        task = TaskNumber.query.filter_by(number=i).first()
        if not task:
            task = TaskNumber(number=i)
            db.session.add(task)

    # Создаем пользователей
    users_data = [
        {
            "username": "makarkonev",
            "role": "super_admin",
            "first_name": "Макар",
            "last_name": "Конев",
        },
        {
            "username": "katherinevstheworld",
            "role": "super_admin",
            "first_name": "Катерина",
            "last_name": "Бриль",
        },
        {
            "username": "zinger_s",
            "role": "admin",
            "first_name": "Александра",
            "last_name": "Смирнова",
        },
        {
            "username": "firstdarksoul",
            "role": "admin",
            "first_name": "Максим",
            "last_name": "Михеев",
        },
        {
            "username": "velukayataina",
            "role": "admin",
            "first_name": "Таина",
            "last_name": "Житина",
        },
        {
            "username": "mkhorinova",
            "role": "regular",
            "first_name": "Муслима",
            "last_name": "Хоринова",
        },
        {
            "username": "pollliin",
            "role": "regular",
            "first_name": "Полина",
            "last_name": "Гусева",
        },
        {
            "username": "lllsbp",
            "role": "regular",
            "first_name": "Самира",
            "last_name": "Шигалугова",
        },
        {
            "username": "elya_na_svyazi",
            "role": "regular",
            "first_name": "Элина",
            "last_name": "Аметова",
        },
        {
            "username": "arr_niga",
            "role": "regular",
            "first_name": "Артём",
            "last_name": "Нигматулин",
        },
        {
            "username": "dariashupikova",
            "role": "regular",
            "first_name": "Дарья",
            "last_name": "Шупикова",
        },
        {
            "username": "amalia_m_21",
            "role": "regular",
            "first_name": "Амалия",
            "last_name": "Мордвинова",
        },
    ]

    for user_data in users_data:
        username = user_data["username"]
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(
                username=username,
                role=user_data["role"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
            )
            user.set_password("123456")  
            db.session.add(user)

    db.session.commit()
    print("База данных успешно инициализирована!")


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True) 