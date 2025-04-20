from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Константы для ролей
ROLE_EDUCATIONAL_CURATOR = 'educational_curator'
ROLE_ORGANIZATIONAL_CURATOR = 'organizational_curator'
ROLE_ADMIN = 'admin'
ROLE_SUPER_ADMIN = 'super_admin'

# Модель для вебинаров
class Webinar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date)
    task_numbers = db.relationship(
        "TaskNumber", secondary="webinar_task_association", back_populates="webinars"
    )
    is_programming = db.Column(db.Boolean, default=False)  # Решение прогой
    is_manual = db.Column(db.Boolean, default=False)  # Решение руками
    is_excel = db.Column(db.Boolean, default=False)  # Решение в Excel
    homework_number = db.Column(db.Integer)
    category = db.Column(db.Integer)  # 1: Обязательный, 2: Повторение, 3: Не обязательный, 4: Для продвинутых
    for_beginners = db.Column(db.Boolean, default=False)  # Курс Python с нуля
    for_basic = db.Column(db.Boolean, default=False)  # Основной курс
    for_advanced = db.Column(db.Boolean, default=False)  # Хард прога
    for_expert = db.Column(db.Boolean, default=False)  # Задание 27
    for_mocks = db.Column(db.Boolean, default=False)  # Разбор пробников
    for_practice = db.Column(db.Boolean, default=False)  # Нарешка
    for_minisnap = db.Column(db.Boolean, default=False)  # Мини-щелчок
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # ID создателя
    created_by = db.relationship("User")
    comments = db.relationship(
        "WebinarComment", backref="webinar", cascade="all, delete-orphan"
    )
    cover_url = db.Column(db.String(500))  # Ссылка на обложку

    planned_in = db.relationship("PlannedWebinar", back_populates="webinar")
    watched_by = db.relationship("WatchedWebinar", back_populates="webinar")
    tasks = db.relationship(
        "WebinarTask", backref="webinar", cascade="all, delete-orphan"
    )

    # Добавляем именованное ограничение уникальности для URL
    __table_args__ = (db.UniqueConstraint("url", name="uq_webinar_url"),)


# Модель для задач к вебинару
class WebinarTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)  # Текст задачи
    webinar_id = db.Column(db.Integer, db.ForeignKey("webinar.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # ID пользователя, добавившего задачу

    created_by = db.relationship("User")


# Модель для номеров заданий
class TaskNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    webinars = db.relationship(
        "Webinar", secondary="webinar_task_association", back_populates="task_numbers"
    )


# Ассоциативная таблица для связи вебинаров и номеров заданий
webinar_task_association = db.Table(
    "webinar_task_association",
    db.Column("webinar_id", db.Integer, db.ForeignKey("webinar.id"), primary_key=True),
    db.Column(
        "task_number_id", db.Integer, db.ForeignKey("task_number.id"), primary_key=True
    ),
)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    platform_id = db.Column(db.String(100), nullable=False, index=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_score = db.Column(db.Integer)
    hours_per_week = db.Column(db.Integer)
    known_tasks = db.relationship(
        "KnownTaskNumber",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    last_plan_id = db.Column(db.Integer, db.ForeignKey("study_plan.id"), nullable=True)
    plans = db.relationship(
        "StudyPlan", back_populates="student", foreign_keys="StudyPlan.student_id"
    )
    watched_webinars = db.relationship("WatchedWebinar", back_populates="student")
    notes = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    initial_score = db.Column(db.Integer, nullable=True)
    needs_python_basics = db.Column(db.Boolean, default=False)
    task_26_deferred = db.Column(db.Boolean, default=False)
    task_27_deferred = db.Column(db.Boolean, default=False)

    @property
    def full_name(self):
        parts = [self.first_name, self.last_name]
        return " ".join(p for p in parts if p)

    @property
    def is_beginner(self):
        """Проверяет, является ли студент начинающим на основе needs_python_basics."""
        return self.needs_python_basics


# Модель для планов обучения
class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # ID создателя

    student = db.relationship(
        "Student", back_populates="plans", foreign_keys=[student_id]
    )
    planned_webinars = db.relationship(
        "PlannedWebinar", back_populates="study_plan", cascade="all, delete-orphan"
    )
    created_by = db.relationship("User")


# Модель для запланированных вебинаров в плане
class PlannedWebinar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_plan_id = db.Column(
        db.Integer, db.ForeignKey("study_plan.id"), nullable=False
    )
    webinar_id = db.Column(db.Integer, db.ForeignKey("webinar.id"), nullable=False)
    week_number = db.Column(db.Integer, nullable=False, default=1)  # Номер недели (1-5)

    study_plan = db.relationship("StudyPlan", back_populates="planned_webinars")
    webinar = db.relationship("Webinar", back_populates="planned_in")


# Модель для просмотренных вебинаров
class WatchedWebinar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    webinar_id = db.Column(db.Integer, db.ForeignKey("webinar.id"), nullable=False)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # ID пользователя, который отметил

    student = db.relationship("Student", back_populates="watched_webinars")
    webinar = db.relationship("Webinar", back_populates="watched_by")
    created_by = db.relationship("User")


# Модель для известных заданий студента
class KnownTaskNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    task_number = db.Column(db.Integer, nullable=False)  # Номер задания

    student = db.relationship("Student", back_populates="known_tasks")


# Модель для пользователей (кураторов, администраторов)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # Обновляем поле role
    role = db.Column(db.String(50), nullable=False, default=ROLE_ORGANIZATIONAL_CURATOR)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def full_name(self):
        parts = [self.first_name, self.last_name]
        return " ".join(p for p in parts if p)

    @property
    def is_admin(self):
        # Только admin и super_admin являются администраторами
        return self.role in [ROLE_ADMIN, ROLE_SUPER_ADMIN]

    @property
    def is_super_admin(self):
        return self.role == ROLE_SUPER_ADMIN

    # Новые свойства для удобства
    @property
    def is_organizational_curator(self):
        return self.role == ROLE_ORGANIZATIONAL_CURATOR

    @property
    def is_educational_curator(self):
        return self.role == ROLE_EDUCATIONAL_CURATOR

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


# Модель для комментариев к вебинарам
class WebinarComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    webinar_id = db.Column(db.Integer, db.ForeignKey("webinar.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User")
