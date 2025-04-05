from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class StudentForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=64)])
    platform_id = StringField('ID на платформе Школково', validators=[DataRequired(), Length(max=100)])
    target_score = IntegerField('Целевой балл', validators=[DataRequired(), NumberRange(min=60, max=100, message='Введите балл от 60 до 100')])
    initial_score = IntegerField('Балл за последний пробник (если есть)', validators=[Optional(), NumberRange(min=0, max=100, message='Введите балл от 0 до 100')])
    hours_per_week = IntegerField('Часов на информатику в неделю', validators=[DataRequired(), NumberRange(min=1, message='Укажите хотя бы 1 час')])
    needs_python_basics = BooleanField('Нужен курс Python с нуля?')
    notes = TextAreaField('Заметки', validators=[Optional()])
    submit = SubmitField('Сохранить')

# Закомментируем неиспользуемую/недописанную форму
# class AssignTasksForm(FlaskForm):
