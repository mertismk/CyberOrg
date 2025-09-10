from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from uuid import uuid4

from app.models import db, UpdateNotification, UserNotificationStatus, UpdateNotificationImage, User
from app.updates import bp
from app import super_admin_required
from sqlalchemy import func


@bp.route('/manage')
@login_required
@super_admin_required
def manage_updates():
    """Страница управления уведомлениями об обновлениях."""
    notifications = UpdateNotification.query.order_by(UpdateNotification.created_at.desc()).all()
    return render_template('updates/manage_updates.html', notifications=notifications)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@super_admin_required
def create_update():
    """Создание нового уведомления об обновлении."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        version = request.form.get('version')
        priority = int(request.form.get('priority', 1))
        show_until = request.form.get('show_until')
        background_color = request.form.get('background_color', '#667eea')
        text_color = request.form.get('text_color', '#ffffff')
        icon = request.form.get('icon', 'rocket')
        
        if not title or not content:
            flash('Заголовок и содержание обязательны для заполнения.', 'error')
            return render_template('updates/update_form.html')
        
        # Создание уведомления
        notification = UpdateNotification(
            title=title,
            content=content,
            version=version,
            priority=priority,
            background_color=background_color,
            text_color=text_color,
            icon=icon,
            created_by_id=current_user.id,
            show_until=datetime.strptime(show_until, '%Y-%m-%d') if show_until else None
        )
        
        db.session.add(notification)
        db.session.flush()  # Получаем ID уведомления
        
        # Обработка загрузки множественных изображений
        images = request.files.getlist('images')
        captions = request.form.getlist('image_captions')
        
        for i, image_file in enumerate(images):
            if image_file and image_file.filename and allowed_file(image_file.filename):
                # Создаем уникальное имя файла
                filename = str(uuid4()) + '.' + image_file.filename.rsplit('.', 1)[1].lower()
                
                # Создаем папку если её нет
                upload_folder = os.path.join(current_app.static_folder, 'uploads', 'update_images')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Сохраняем файл
                file_path = os.path.join(upload_folder, filename)
                image_file.save(file_path)
                
                # Создаем запись изображения
                notification_image = UpdateNotificationImage(
                    notification_id=notification.id,
                    image_url=f'uploads/update_images/{filename}',
                    caption=captions[i] if i < len(captions) and captions[i] else None,
                    position=i
                )
                db.session.add(notification_image)
        
        db.session.add(notification)
        db.session.commit()
        
        flash('Уведомление об обновлении успешно создано!', 'success')
        return redirect(url_for('updates.manage_updates'))
    
    return render_template('updates/update_form.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@super_admin_required
def edit_update(id):
    """Редактирование уведомления об обновлении."""
    notification = UpdateNotification.query.get_or_404(id)
    
    if request.method == 'POST':
        notification.title = request.form.get('title')
        notification.content = request.form.get('content')
        notification.version = request.form.get('version')
        notification.priority = int(request.form.get('priority', 1))
        notification.is_active = 'is_active' in request.form
        notification.background_color = request.form.get('background_color', notification.background_color)
        notification.text_color = request.form.get('text_color', notification.text_color)
        notification.icon = request.form.get('icon', notification.icon)
        notification.updated_at = datetime.utcnow()
        
        show_until = request.form.get('show_until')
        notification.show_until = datetime.strptime(show_until, '%Y-%m-%d') if show_until else None
        
        # Обработка удаления изображений
        images_to_delete = request.form.getlist('delete_images')
        for image_id in images_to_delete:
            image = UpdateNotificationImage.query.get(image_id)
            if image and image.notification_id == notification.id:
                # Удаляем файл
                image_path = os.path.join(current_app.static_folder, image.image_url)
                if os.path.exists(image_path):
                    os.remove(image_path)
                db.session.delete(image)
        
        # Обработка новых изображений
        images = request.files.getlist('images')
        captions = request.form.getlist('image_captions')
        
        # Получаем максимальную позицию для новых изображений
        max_position = db.session.query(func.max(UpdateNotificationImage.position)).filter_by(
            notification_id=notification.id
        ).scalar() or -1
        
        for i, image_file in enumerate(images):
            if image_file and image_file.filename and allowed_file(image_file.filename):
                # Создаем уникальное имя файла
                filename = str(uuid4()) + '.' + image_file.filename.rsplit('.', 1)[1].lower()
                
                # Создаем папку если её нет
                upload_folder = os.path.join(current_app.static_folder, 'uploads', 'update_images')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Сохраняем файл
                file_path = os.path.join(upload_folder, filename)
                image_file.save(file_path)
                
                # Создаем запись изображения
                notification_image = UpdateNotificationImage(
                    notification_id=notification.id,
                    image_url=f'uploads/update_images/{filename}',
                    caption=captions[i] if i < len(captions) and captions[i] else None,
                    position=max_position + 1 + i
                )
                db.session.add(notification_image)
        
        db.session.commit()
        flash('Уведомление об обновлении успешно обновлено!', 'success')
        return redirect(url_for('updates.manage_updates'))
    
    return render_template('updates/update_form.html', notification=notification)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@super_admin_required
def delete_update(id):
    """Удаление уведомления об обновлении."""
    notification = UpdateNotification.query.get_or_404(id)
    
    # Удаляем все изображения уведомления
    for image in notification.images:
        image_path = os.path.join(current_app.static_folder, image.image_url)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    # Удаляем все статусы пользователей для этого уведомления
    UserNotificationStatus.query.filter_by(notification_id=id).delete()
    
    db.session.delete(notification)
    db.session.commit()
    
    flash('Уведомление об обновлении удалено!', 'success')
    return redirect(url_for('updates.manage_updates'))


@bp.route('/history')
@login_required
def updates_history():
    """Страница истории обновлений для всех пользователей."""
    page = request.args.get('page', 1, type=int)
    notifications = UpdateNotification.query.filter_by(is_active=True).order_by(
        UpdateNotification.created_at.desc()
    ).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('updates/history.html', notifications=notifications)


@bp.route('/api/unread')
@login_required
def get_unread_notifications():
    """API для получения непрочитанных уведомлений текущего пользователя."""
    # Получаем ID уведомлений, которые пользователь уже видел
    viewed_notification_ids = db.session.query(UserNotificationStatus.notification_id).filter_by(
        user_id=current_user.id
    ).subquery()
    
    # Получаем активные уведомления, которые пользователь ещё не видел
    unread_notifications = UpdateNotification.query.filter(
        UpdateNotification.is_active == True,
        ~UpdateNotification.id.in_(viewed_notification_ids),
        db.or_(
            UpdateNotification.show_until.is_(None),
            UpdateNotification.show_until > datetime.utcnow()
        )
    ).order_by(
        UpdateNotification.priority.desc(),
        UpdateNotification.created_at.desc()
    ).all()
    
    # Преобразуем в JSON
    notifications_data = []
    for notification in unread_notifications:
        # Собираем изображения
        images_data = []
        for image in notification.images:
            images_data.append({
                'image_url': image.image_url,
                'caption': image.caption,
                'position': image.position
            })
        
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'content': notification.content,
            'version': notification.version,
            'images': images_data,
            'priority': notification.priority,
            'background_color': notification.background_color,
            'text_color': notification.text_color,
            'icon': notification.icon,
            'created_at': notification.created_at.isoformat()
        })
    
    return jsonify(notifications_data)


@bp.route('/api/mark_viewed/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_viewed(notification_id):
    """API для отметки уведомления как просмотренного."""
    # Проверяем, что уведомление существует
    notification = UpdateNotification.query.get_or_404(notification_id)
    
    # Проверяем, не отмечено ли уже как просмотренное
    existing_status = UserNotificationStatus.query.filter_by(
        user_id=current_user.id,
        notification_id=notification_id
    ).first()
    
    if not existing_status:
        # Создаем новый статус
        status = UserNotificationStatus(
            user_id=current_user.id,
            notification_id=notification_id
        )
        db.session.add(status)
        db.session.commit()
    
    return jsonify({'status': 'success'})


@bp.route('/resend/<int:notification_id>', methods=['POST'])
@login_required
@super_admin_required
def resend_notification(notification_id):
    """Повторная отправка уведомления всем пользователям (очистка статусов просмотра)."""
    notification = UpdateNotification.query.get_or_404(notification_id)
    
    # Удаляем все статусы просмотра для этого уведомления
    deleted_count = UserNotificationStatus.query.filter_by(notification_id=notification_id).delete()
    db.session.commit()
    
    flash(f'Уведомление "{notification.title}" отправлено всем пользователям повторно! Очищено {deleted_count} записей о просмотре.', 'success')
    return redirect(url_for('updates.manage_updates'))


@bp.route('/statistics')
@login_required
@super_admin_required
def notification_statistics():
    """Страница статистики просмотров уведомлений."""
    page = request.args.get('page', 1, type=int)
    notification_id = request.args.get('notification_id', type=int)
    
    # Базовый запрос
    query = UpdateNotification.query
    
    # Фильтрация по конкретному уведомлению
    if notification_id:
        query = query.filter_by(id=notification_id)
    
    notifications = query.order_by(
        UpdateNotification.created_at.desc()
    ).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Собираем статистику для каждого уведомления
    stats_data = []
    for notification in notifications.items:
        # Получаем всех пользователей, просмотревших это уведомление
        viewed_users = db.session.query(UserNotificationStatus, User).join(
            User, UserNotificationStatus.user_id == User.id
        ).filter(
            UserNotificationStatus.notification_id == notification.id
        ).order_by(UserNotificationStatus.viewed_at.desc()).all()
        
        stats_data.append({
            'notification': notification,
            'viewed_users': viewed_users,
            'total_views': len(viewed_users)
        })
    
    return render_template(
        'updates/statistics.html',
        notifications=notifications,
        stats_data=stats_data,
        current_notification_id=notification_id
    )


@bp.route('/statistics/<int:notification_id>')
@login_required
@super_admin_required
def notification_detailed_stats(notification_id):
    """Детальная статистика конкретного уведомления."""
    notification = UpdateNotification.query.get_or_404(notification_id)
    
    # Получаем всех пользователей, просмотревших это уведомление
    viewed_users = db.session.query(UserNotificationStatus, User).join(
        User, UserNotificationStatus.user_id == User.id
    ).filter(
        UserNotificationStatus.notification_id == notification_id
    ).order_by(UserNotificationStatus.viewed_at.desc()).all()
    
    # Получаем всех пользователей, которые НЕ просмотрели уведомление
    viewed_user_ids = [status.user_id for status, user in viewed_users]
    not_viewed_users = User.query.filter(
        ~User.id.in_(viewed_user_ids)
    ).order_by(User.last_login.desc()).all() if viewed_user_ids else User.query.order_by(User.last_login.desc()).all()
    
    return render_template(
        'updates/detailed_statistics.html',
        notification=notification,
        viewed_users=viewed_users,
        not_viewed_users=not_viewed_users,
        now=datetime.utcnow()
    )


def allowed_file(filename):
    """Проверяет, разрешен ли тип файла для загрузки."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
