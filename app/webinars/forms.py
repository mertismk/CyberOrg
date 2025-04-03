from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Optional, URL, ValidationError
import re

# Choices for categories
CATEGORY_CHOICES = [('', 'Не выбрана'), ('1', 'Обязательный'), ('2', 'Повторение'), ('3', 'Необязательный')]
COURSE_CATEGORY_CHOICES = [
    ('', 'Не выбрана'),
    ('python с нуля', 'Python с нуля'),
    ('основной курс', 'Основной курс'),
    ('хард прога', 'Хард прога'),
    ('задание 27', 'Задание 27'),
    ('разбор пробников', 'Разбор пробников'),
    ('нарешка', 'Нарешка'),
    ('мини-щелчок', 'Мини-щелчок')
]

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

    # Используем отдельные чекбоксы для типа решения
    is_programming = BooleanField('Программное решение')
    is_manual = BooleanField('Ручное решение')

    category = SelectField('Категория', choices=CATEGORY_CHOICES, validators=[Optional()])

    # Используем SelectField для категории курса
    course_category = SelectField('Категория курса', choices=COURSE_CATEGORY_CHOICES, validators=[Optional()])

    cover_url = StringField('Ссылка на обложку', validators=[Optional(), URL(message='Некорректный URL обложки')])

    submit = SubmitField('Сохранить изменения') 