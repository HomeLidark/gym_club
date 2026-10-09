from django.contrib import admin
from .models import Member, DailyAttendance


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'id_number', 'subscription_end', 'is_active', 'is_expired')
    list_filter = ('is_active', 'subscription_type', 'subscription_end')
    search_fields = ('name', 'phone', 'id_number')
    ordering = ('-join_date',)
    readonly_fields = ('join_date',)


@admin.register(DailyAttendance)
class DailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'check_in_date', 'check_in_time')
    list_filter = ('check_in_date',)
    search_fields = ('member__name',)
    ordering = ('-check_in_date', '-check_in_time')