from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional, URL, ValidationError
import re
from datetime import datetime

# Обновленные Choices for categories
CATEGORY_CHOICES = [
    ('', 'Не выбрана'), 
    ('1', 'Обязательный'), 
    ('2', 'Повторение'), 
    ('3', 'Не обязательный'), 
    ('4', 'Для продвинутых') # Добавлена категория 4
]

# Choices для учебного года
current_year = datetime.now().year
ACADEMIC_YEAR_CHOICES = [(year, str(year)) for year in range(2025, current_year + 2)]

def validate_task_numbers(form, field):
    if field.data:
        nums = field.data.split(',')
        for num_str in nums:
            num_str = num_str.strip()
            if not num_str.isdigit():
                raise ValidationError(f'Неверный формат номера задания: "{num_str}". Номера должны быть числами через запятую.')
            if not 1 <= int(num_str) <= 27:
                raise ValidationError(f'Номер задания "{num_str}" должен быть в диапазоне от 1 до 27.')


class WebinarForm(FlaskForm):
    title = StringField('Название вебинара', validators=[DataRequired()])
    url = StringField('Ссылка на вебинар', validators=[DataRequired(), URL(message='Некорректный URL вебинара')])
    date = DateField('Дата вебинара (ГГГГ-ММ-ДД)', format='%Y-%m-%d', validators=[Optional()])
    task_numbers = StringField('Номера заданий (через запятую)', validators=[Optional(), validate_task_numbers])
    academic_year = SelectField('Учебный год', choices=ACADEMIC_YEAR_CHOICES, coerce=int, default=2026)

    # Чекбоксы для типа решения (без изменений)
    is_programming = BooleanField('Программное решение')
    is_manual = BooleanField('Ручное решение')
    is_excel = BooleanField('Решение в Excel')

    # Категория важности - обновлены choices
    category = SelectField('Категория важности', choices=CATEGORY_CHOICES, coerce=str, validators=[Optional()]) # Используем coerce=str, т.к. choices - строки

    # --- Замена SelectField на BooleanField для Категории Курса --- 
    for_beginners = BooleanField('Python с нуля') 
    for_basic = BooleanField('Основной курс') 
    for_advanced = BooleanField('Задание 26') 
    for_expert = BooleanField('Задание 27') 
    for_mocks = BooleanField('Разбор пробников') 
    for_practice = BooleanField('Нарешка') 
    for_minisnap = BooleanField('Мини-щелчок') 
    for_summer = BooleanField('Летний курс')
    # --- Конец замены --- 

    cover_url = StringField('Ссылка на обложку', validators=[Optional(), URL(message='Некорректный URL обложки')])

    submit = SubmitField('Сохранить изменения')


# Форма для добавления задачи к вебинару
class WebinarTaskForm(FlaskForm):
    text = TextAreaField('Текст задачи', validators=[DataRequired()])
    submit = SubmitField('Добавить задачу') 