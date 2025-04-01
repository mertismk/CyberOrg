from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    # Роли: super_admin, admin, regular
    role = db.Column(db.String(20), default='regular', nullable=False)
    last_login = db.Column(db.DateTime, default=None, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_super_admin(self):
        return self.role == 'super_admin'
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.role == 'super_admin'
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'

class TaskNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    
    def __repr__(self):
        return f'<TaskNumber {self.number}>'

# Таблица связи для отношения многие-ко-многим между вебинарами и номерами заданий
webinar_task_numbers = db.Table('webinar_task_numbers',
    db.Column('webinar_id', db.Integer, db.ForeignKey('webinar.id'), primary_key=True),
    db.Column('task_number_id', db.Integer, db.ForeignKey('task_number.id'), primary_key=True)
)

class Webinar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(255), nullable=True)  # Ссылка на обложку вебинара
    date = db.Column(db.Date, nullable=True)  # Делаем дату опциональной
    is_programming = db.Column(db.Boolean, default=False)  # Программирование
    is_manual = db.Column(db.Boolean, default=False)  # Ручное решение
    homework_number = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.Text, nullable=True)  # Комментарий к вебинару
    
    # Категория вебинара:
    # 1 - обязательный к просмотру (основная теория)
    # 2 - повторение
    # 3 - необязательный (нет ничего нового)
    category = db.Column(db.Integer, nullable=True)
    
    # Связь с номерами заданий
    task_numbers = db.relationship('TaskNumber', secondary=webinar_task_numbers, backref='webinars')
    
    # Для какого уровня подготовки предназначен
    for_beginners = db.Column(db.Boolean, default=False)  # Python с нуля
    for_basic = db.Column(db.Boolean, default=False)  # Основной курс (1-25)
    for_advanced = db.Column(db.Boolean, default=False)  # Хард прога (26)
    for_expert = db.Column(db.Boolean, default=False)  # Задание 27
    
    # Связь с пользователем, создавшим запись
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.relationship('User', backref='created_webinars')
    
    # Связь с комментариями
    comments = db.relationship('WebinarComment', backref='webinar', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Webinar {self.title}>'

class WebinarComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с вебинаром
    webinar_id = db.Column(db.Integer, db.ForeignKey('webinar.id'), nullable=False)
    
    # Связь с пользователем, создавшим комментарий
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='webinar_comments')
    
    def __repr__(self):
        return f'<WebinarComment {self.id} for Webinar {self.webinar_id}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    target_score = db.Column(db.Integer, nullable=True)
    hours_per_week = db.Column(db.Integer, nullable=True)
    
    # Текущий уровень студента
    is_beginner = db.Column(db.Boolean, default=True)
    knows_task_26 = db.Column(db.Boolean, default=False)
    knows_task_27 = db.Column(db.Boolean, default=False)
    
    # Связь с планами обучения
    study_plans = db.relationship('StudyPlan', backref='student', lazy=True)
    
    # Уже просмотренные вебинары
    watched_webinars = db.relationship('WatchedWebinar', backref='student', lazy=True)
    
    # Связь с известными заданиями
    known_task_numbers = db.relationship('KnownTaskNumber', backref='student', lazy=True)
    
    # Связь с пользователем, создавшим запись
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.relationship('User', backref='created_students')
    
    def __repr__(self):
        return f'<Student {self.last_name} {self.first_name}>'

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с запланированными вебинарами
    planned_webinars = db.relationship('PlannedWebinar', backref='study_plan', lazy=True)
    
    # Связь с пользователем, создавшим запись
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.relationship('User', backref='created_plans')
    
    def __repr__(self):
        return f'<StudyPlan {self.id} for Student {self.student_id}>'

class PlannedWebinar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plan.id'), nullable=False)
    webinar_id = db.Column(db.Integer, db.ForeignKey('webinar.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)  # Номер недели в плане (1-5)
    
    # Связь с вебинаром
    webinar = db.relationship('Webinar', backref='planned_in', lazy=True)
    
    def __repr__(self):
        return f'<PlannedWebinar {self.webinar_id} for Week {self.week_number}>'

class WatchedWebinar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    webinar_id = db.Column(db.Integer, db.ForeignKey('webinar.id'), nullable=False)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с вебинаром
    webinar = db.relationship('Webinar', backref='watched_by', lazy=True)
    
    # Связь с пользователем, создавшим запись
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.relationship('User', backref='marked_watched')
    
    def __repr__(self):
        return f'<WatchedWebinar {self.webinar_id} by Student {self.student_id}>'

class KnownTaskNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    task_number = db.Column(db.Integer, nullable=False)
    
    # Уникальность по студенту и номеру задания
    __table_args__ = (db.UniqueConstraint('student_id', 'task_number'),)
    
    def __repr__(self):
        return f'<KnownTaskNumber {self.task_number} for Student {self.student_id}>'
