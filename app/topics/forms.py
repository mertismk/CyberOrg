from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Optional, ValidationError
import re


def validate_task_numbers(form, field):
    """Валидатор для проверки номеров заданий ОГЭ"""
    if field.data:
        # Для ОГЭ номера заданий от 1 до 16
        nums = field.data.split(',')
        for num_str in nums:
            num_str = num_str.strip()
            if not num_str.isdigit():
                raise ValidationError(f'Неверный формат номера задания: "{num_str}". Номера должны быть числами через запятую.')
            task_num = int(num_str)
            if not 1 <= task_num <= 16:
                raise ValidationError(f'Номер задания "{num_str}" должен быть в диапазоне от 1 до 16 для ОГЭ.')


class OGETopicForm(FlaskForm):
    name = StringField('Название темы', validators=[DataRequired()], 
                      render_kw={'placeholder': 'Например: Системы счисления'})
    
    task_numbers_str = StringField('Номера заданий (через запятую)', validators=[Optional(), validate_task_numbers],
                                  render_kw={'placeholder': 'Например: 10 или 1, 2'})
    
    description = TextAreaField('Описание темы', validators=[Optional()],
                               render_kw={'placeholder': 'Краткое описание темы (опционально)', 'rows': 3})
    
    is_active = BooleanField('Активная тема', default=True)
    
    submit = SubmitField('Сохранить')


class OGETopicDeleteForm(FlaskForm):
    """Форма для подтверждения удаления темы"""
    submit = SubmitField('Удалить')
