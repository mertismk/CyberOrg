from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.orm import selectinload

from app import db
from app.models import OGETopic
from app.topics import bp
from app.topics.forms import OGETopicForm, OGETopicDeleteForm


@bp.route("/")
@login_required
def topics_list():
    """Список всех тем ОГЭ"""
    # Получаем все активные темы, отсортированные по названию
    topics = OGETopic.query.filter_by(is_active=True).order_by(OGETopic.name).all()
    
    return render_template(
        "topics/topics_list.html",
        topics=topics
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_topic():
    """Создание новой темы ОГЭ"""
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен
    
    form = OGETopicForm()
    
    if form.validate_on_submit():
        # Проверяем, не существует ли уже тема с таким названием
        existing_topic = OGETopic.query.filter_by(name=form.name.data).first()
        if existing_topic:
            flash('Тема с таким названием уже существует', 'danger')
            return redirect(request.url)
        
        # Создаем новую тему
        topic = OGETopic(
            name=form.name.data,
            task_numbers_str=form.task_numbers_str.data,
            description=form.description.data,
            is_active=form.is_active.data
        )
        
        try:
            db.session.add(topic)
            db.session.commit()
            flash(f'Тема "{topic.name}" успешно создана!', 'success')
            return redirect(url_for('topics.topics_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при создании темы: {str(e)}', 'danger')
    
    return render_template('topics/topic_form.html', 
                         form=form, 
                         mode='create',
                         title='Создание новой темы')


@bp.route("/<int:topic_id>/edit", methods=["GET", "POST"])
@login_required
def edit_topic(topic_id):
    """Редактирование темы ОГЭ"""
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен
    
    topic = OGETopic.query.get_or_404(topic_id)
    form = OGETopicForm(obj=topic)
    
    if form.validate_on_submit():
        # Проверяем, не существует ли уже другая тема с таким названием
        existing_topic = OGETopic.query.filter(
            OGETopic.name == form.name.data,
            OGETopic.id != topic_id
        ).first()
        if existing_topic:
            flash('Тема с таким названием уже существует', 'danger')
            return redirect(request.url)
        
        # Обновляем тему
        topic.name = form.name.data
        topic.task_numbers_str = form.task_numbers_str.data
        topic.description = form.description.data
        topic.is_active = form.is_active.data
        
        try:
            db.session.commit()
            flash(f'Тема "{topic.name}" успешно обновлена!', 'success')
            return redirect(url_for('topics.topics_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении темы: {str(e)}', 'danger')
    
    return render_template('topics/topic_form.html', 
                         form=form, 
                         topic=topic,
                         mode='edit',
                         title=f'Редактирование темы "{topic.name}"')


@bp.route("/<int:topic_id>/delete", methods=["GET", "POST"])
@login_required
def delete_topic(topic_id):
    """Удаление темы ОГЭ"""
    if not current_user.is_admin:
        abort(403)  # Доступ запрещен
    
    topic = OGETopic.query.options(
        selectinload(OGETopic.webinars)
    ).get_or_404(topic_id)
    
    form = OGETopicDeleteForm()
    
    if form.validate_on_submit():
        # Проверяем, есть ли связанные вебинары
        if topic.webinars:
            flash(f'Нельзя удалить тему "{topic.name}", так как она используется в {len(topic.webinars)} вебинарах. '
                  f'Сначала отвяжите тему от вебинаров или деактивируйте её.', 'danger')
            return redirect(url_for('topics.topics_list'))
        
        topic_name = topic.name
        try:
            db.session.delete(topic)
            db.session.commit()
            flash(f'Тема "{topic_name}" успешно удалена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при удалении темы: {str(e)}', 'danger')
        
        return redirect(url_for('topics.topics_list'))
    
    return render_template('topics/confirm_delete.html', 
                         topic=topic, 
                         form=form)


@bp.route("/<int:topic_id>/detail")
@login_required
def topic_detail(topic_id):
    """Детальная информация о теме и связанных вебинарах"""
    topic = OGETopic.query.options(
        selectinload(OGETopic.webinars)
    ).get_or_404(topic_id)
    
    return render_template('topics/topic_detail.html', topic=topic)


@bp.route("/all")
@login_required
def all_topics():
    """Список всех тем (включая неактивные) - для админов"""
    if not current_user.is_admin:
        abort(403)
    
    topics = OGETopic.query.order_by(OGETopic.name).all()
    
    return render_template(
        "topics/topics_list.html",
        topics=topics,
        show_all=True
    )
