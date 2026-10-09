// ============================================================
// =================== سكريبتات الموقع ========================
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ====== إخفاء التنبيهات تلقائياً ======
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });
    
    // ====== تأكيد الحذف ======
    const deleteButtons = document.querySelectorAll('.delete-confirm, .btn-danger[onclick*="delete"]');
    deleteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('⚠️ هل أنت متأكد من الحذف؟ هذا الإجراء لا يمكن التراجع عنه!')) {
                e.preventDefault();
            }
        });
    });
    
    // ====== تفعيل الـ Tooltips ======
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ====== تفعيل الـ Popovers ======
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // ====== بحث سريع ======
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                this.closest('form').submit();
            }
        });
    }
    
    // ====== تحديد تاريخ في التقارير ======
    const monthSelect = document.getElementById('month-select');
    const yearSelect = document.getElementById('year-select');
    
    if (monthSelect && yearSelect) {
        monthSelect.addEventListener('change', function() {
            window.location.href = `?month=${this.value}&year=${yearSelect.value}`;
        });
        
        yearSelect.addEventListener('change', function() {
            window.location.href = `?month=${monthSelect.value}&year=${this.value}`;
        });
    }
    
    // ====== إضافة تأثير للبطاقات ======
    const cards = document.querySelectorAll('.card:not(.no-hover)');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
    
    // ====== تظليل الصفوف في الجداول ======
    const tables = document.querySelectorAll('.table-hover');
    tables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row, index) {
            if (index % 2 === 0) {
                row.style.backgroundColor = 'transparent';
            }
        });
    });
});

// ============================================================
// =================== دوال عامة ==============================
// ============================================================

// ====== طباعة الصفحة ======
function printPage() {
    window.print();
}

// ====== تصدير الجدول إلى CSV ======
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(function(row) {
        const rowData = [];
        const cols = row.querySelectorAll('td, th');
        cols.forEach(function(col) {
            let text = col.textContent.trim();
            // إزالة الفواصل الزائدة
            text = text.replace(/,/g, '');
            rowData.push(text);
        });
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'report.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// ====== تصدير الجدول إلى Excel (HTML) ======
function exportTableToExcel(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const html = table.outerHTML;
    const blob = new Blob(['\uFEFF' + html], { type: 'application/vnd.ms-excel' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'report.xls';
    a.click();
    window.URL.revokeObjectURL(url);
}

// ====== عرض رسالة نجاح ======
function showSuccess(message) {
    showAlert(message, 'success');
}

// ====== عرض رسالة خطأ ======
function showError(message) {
    showAlert(message, 'error');
}

// ====== عرض رسالة تحذير ======
function showWarning(message) {
    showAlert(message, 'warning');
}

// ====== عرض رسالة معلومات ======
function showInfo(message) {
    showAlert(message, 'info');
}

// ====== دالة مساعدة لعرض التنبيهات ======
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 
                        type === 'error' ? 'exclamation-circle' : 
                        type === 'warning' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.main-content');
    if (container) {
        const firstChild = container.firstChild;
        container.insertBefore(alertDiv, firstChild);
        
        // إخفاء بعد 5 ثواني
        setTimeout(function() {
            const closeBtn = alertDiv.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    }
}