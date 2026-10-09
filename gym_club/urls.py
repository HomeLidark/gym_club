"""
URL configuration for gym_club project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from members import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ===== مسارات تسجيل الدخول =====
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ===== مسارات لوحة التحكم =====
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ===== مسارات الأعضاء =====
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.add_member, name='add_member'),
    path('members/edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('members/delete/<int:member_id>/', views.delete_member, name='delete_member'),
    
    # ===== مسارات الحضور =====
    path('attendance/', views.attendance, name='attendance'),
    
    # ===== مسارات التنبيهات =====
    path('alerts/', views.renewal_alerts, name='renewal_alerts'),
    path('alerts/count/', views.alert_count, name='alert_count'),
    
    # ===== مسارات التقارير =====
    path('reports/', views.reports, name='reports'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),  # أضف هذا
    # ===== مسارات تجميد الاشتراك =====
    path('members/freeze/<int:member_id>/', views.freeze_member, name='freeze_member'),
    path('members/unfreeze/<int:member_id>/', views.unfreeze_member, name='unfreeze_member'),



]