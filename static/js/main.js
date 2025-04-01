// Инициализация скриптов при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое скрытие сообщений об успехе/ошибке через 5 секунд
    const alerts = document.querySelectorAll('.alert:not(.alert-warning):not(.alert-info)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade');
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // Добавление кнопок "Выбрать все" / "Снять выбор" для чекбоксов
    const checkboxGroups = document.querySelectorAll('.checkbox-group');
    checkboxGroups.forEach(function(group) {
        const checkboxes = group.querySelectorAll('input[type="checkbox"]');
        if (checkboxes.length > 5) {
            const selectAllBtn = document.createElement('button');
            selectAllBtn.type = 'button';
            selectAllBtn.className = 'btn btn-sm btn-outline-primary me-2';
            selectAllBtn.textContent = 'Выбрать все';
            selectAllBtn.addEventListener('click', function() {
                checkboxes.forEach(function(checkbox) {
                    checkbox.checked = true;
                    // Активируем связанные элементы, если они есть
                    const relatedSelect = checkbox.closest('tr')?.querySelector('select');
                    if (relatedSelect) {
                        relatedSelect.disabled = false;
                    }
                });
            });
            
            const deselectAllBtn = document.createElement('button');
            deselectAllBtn.type = 'button';
            deselectAllBtn.className = 'btn btn-sm btn-outline-secondary';
            deselectAllBtn.textContent = 'Снять выбор';
            deselectAllBtn.addEventListener('click', function() {
                checkboxes.forEach(function(checkbox) {
                    checkbox.checked = false;
                    // Деактивируем связанные элементы, если они есть
                    const relatedSelect = checkbox.closest('tr')?.querySelector('select');
                    if (relatedSelect) {
                        relatedSelect.disabled = true;
                    }
                });
            });
            
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'd-flex justify-content-end mb-3';
            buttonContainer.appendChild(selectAllBtn);
            buttonContainer.appendChild(deselectAllBtn);
            
            group.insertBefore(buttonContainer, group.firstChild);
        }
    });
    
    // Инициализация тултипов Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Функция для фильтрации таблиц
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (input && table) {
        input.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
}

// Функция для обновления недель в плане обучения
function updateWeeks() {
    const selectedWebinars = document.querySelectorAll('input[name="webinar_ids"]:checked');
    let weekCounter = {};
    
    // Сначала подсчитываем количество вебинаров на каждую неделю
    selectedWebinars.forEach(function(checkbox) {
        const weekSelect = checkbox.closest('tr').querySelector('select[name="week_numbers"]');
        const weekNumber = weekSelect.value;
        
        if (!weekCounter[weekNumber]) {
            weekCounter[weekNumber] = 0;
        }
        
        weekCounter[weekNumber]++;
    });
    
    // Проверяем, не превышает ли количество вебинаров в неделю максимальное значение
    const maxWeeklyWebinars = parseInt(document.getElementById('max_weekly_webinars')?.value || 6);
    
    for (const week in weekCounter) {
        if (weekCounter[week] > maxWeeklyWebinars) {
            alert(`Внимание! На неделю ${week} назначено ${weekCounter[week]} вебинаров, что превышает рекомендуемое количество (${maxWeeklyWebinars}).`);
        }
    }
}

// Функция для добавления подтверждения перед удалением важных элементов
function confirmDelete(message) {
    return confirm(message || 'Вы уверены, что хотите удалить этот элемент?');
} 