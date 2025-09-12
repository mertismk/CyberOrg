from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from app.models import db, MaintenanceMode
from . import bp


@bp.route('/maintenance')
@login_required
def maintenance():
    """Страница управления режимом технического обслуживания"""
    if not current_user.is_super_admin:
        flash("У вас нет прав доступа к этой странице.", "danger")
        return redirect(url_for("main.index"))
    
    maintenance = MaintenanceMode.query.first()
    if not maintenance:
        # Создаем запись, если её нет
        maintenance = MaintenanceMode()
        db.session.add(maintenance)
        db.session.commit()
    
    return render_template('admin/maintenance.html', maintenance=maintenance)


@bp.route('/maintenance/toggle', methods=['POST'])
@login_required
def toggle_maintenance():
    """Включение/отключение режима технического обслуживания"""
    if not current_user.is_super_admin:
        flash("У вас нет прав доступа к этой странице.", "danger")
        return redirect(url_for("main.index"))
    
    maintenance = MaintenanceMode.query.first()
    if not maintenance:
        maintenance = MaintenanceMode()
        db.session.add(maintenance)
    
    if maintenance.is_enabled:
        # Отключаем режим обслуживания
        maintenance.disable()
        message = "Режим технического обслуживания отключен"
        flash(message, "success")
    else:
        # Включаем режим обслуживания
        maintenance.enable(current_user.id)
        message = "Режим технического обслуживания включен"
        flash(message, "warning")
    
    db.session.commit()
    
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({
            'success': True,
            'message': message,
            'is_enabled': maintenance.is_enabled
        })
    
    return redirect(url_for('admin.maintenance'))


@bp.route('/maintenance/update_message', methods=['POST'])
@login_required
def update_maintenance_message():
    """Обновление сообщения для режима обслуживания"""
    if not current_user.is_super_admin:
        flash("У вас нет прав доступа к этой странице.", "danger")
        return redirect(url_for("main.index"))
    
    maintenance = MaintenanceMode.query.first()
    if not maintenance:
        maintenance = MaintenanceMode()
        db.session.add(maintenance)
    
    new_message = request.form.get('message', '').strip()
    if new_message:
        maintenance.message = new_message
        db.session.commit()
        flash("Сообщение обновлено", "success")
    else:
        flash("Сообщение не может быть пустым", "danger")
    
    return redirect(url_for('admin.maintenance'))
