from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # ===== صفحات تسجيل الدخول والخروج =====
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ===== لوحة التحكم =====
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ===== إدارة الأعضاء =====
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.add_member, name='add_member'),
    path('members/edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('members/delete/<int:member_id>/', views.delete_member, name='delete_member'),
    
    # ===== تسجيل الدخول اليومي =====
    path('attendance/', views.attendance, name='attendance'),
    
    # ===== تنبيهات التجديد =====
    path('alerts/', views.renewal_alerts, name='renewal_alerts'),
    path('alerts/count/', views.alert_count, name='alert_count'),
    
    # ===== التقارير =====
    path('reports/', views.reports, name='reports'),
]