from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class StudentForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=64)])
    platform_id = StringField('ID на платформе Школково', validators=[DataRequired(), Length(max=100)])
    academic_year = SelectField('Учебный год', choices=[(2026, '2026'), (2025, '2025')], coerce=int, default=2026)
    exam_type = SelectField('Тип экзамена', choices=[('ege', 'ЕГЭ'), ('oge', 'ОГЭ')], default='ege')
    target_score = IntegerField('Целевой балл', validators=[DataRequired(), NumberRange(min=60, max=100, message='Введите балл от 60 до 100')])
    initial_score = IntegerField('Балл за последний пробник (если есть)', validators=[Optional(), NumberRange(min=0, max=100, message='Введите балл от 0 до 100')])
    hours_per_week = IntegerField('Часов на информатику в неделю', validators=[DataRequired(), NumberRange(min=1, message='Укажите хотя бы 1 час')])
    notes = TextAreaField('Заметки', validators=[Optional()])
    # Новые поля для ЕГЭ учеников
    grade = SelectField('Класс', choices=[(10, '10 класс'), (11, '11 класс')], coerce=int, validators=[Optional()])
    tariff = SelectField('Тариф', choices=[('all_inclusive', 'Все включено'), ('self_check', 'Самопроверка')], validators=[Optional()])
    course = SelectField('Курс', choices=[('yearly', 'Годовой')], default='yearly', validators=[Optional()])
    submit = SubmitField('Сохранить')
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        # Динамически обновляем валидаторы в зависимости от типа экзамена
        self._update_validators()
    
    def _update_validators(self):
        """Обновляет валидаторы полей в зависимости от типа экзамена"""
        if hasattr(self, 'exam_type') and self.exam_type.data == 'oge':
            # Для ОГЭ: целевая оценка от 3 до 5
            self.target_score.label.text = 'Целевая оценка'
            self.target_score.validators = [DataRequired(), NumberRange(min=3, max=5, message='Введите оценку от 3 до 5')]
            # Для ОГЭ новые поля не обязательны
            self.grade.validators = [Optional()]
            self.tariff.validators = [Optional()]
            self.course.validators = [Optional()]
        else:
            # Для ЕГЭ: целевой балл от 60 до 100
            self.target_score.label.text = 'Целевой балл'
            self.target_score.validators = [DataRequired(), NumberRange(min=60, max=100, message='Введите балл от 60 до 100')]
            # Для ЕГЭ новые поля обязательны
            self.grade.validators = [DataRequired()]
            self.tariff.validators = [DataRequired()]
            self.course.validators = [DataRequired()]
    
    def validate(self, extra_validators=None):
        """Переопределяем валидацию для динамического обновления валидаторов"""
        self._update_validators()
        return super(StudentForm, self).validate(extra_validators)

# Закомментируем неиспользуемую/недописанную форму
# class AssignTasksForm(FlaskForm):
