from django.db import models
from datetime import date, timedelta


class Member(models.Model):
    # معلومات شخصية
    name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(max_length=15, verbose_name="الهاتف")
    id_number = models.CharField(max_length=20, unique=True, verbose_name="رقم الهوية")
    address = models.TextField(blank=True, verbose_name="العنوان")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    join_date = models.DateField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    
    # معلومات الاشتراك
    subscription_start = models.DateField(verbose_name="بداية الاشتراك")
    subscription_end = models.DateField(verbose_name="نهاية الاشتراك")
    subscription_type = models.CharField(
        max_length=50,
        choices=[
            ('monthly', 'شهري'),
            ('quarterly', 'ثلاثة أشهر'),
            ('yearly', 'سنوي'),
        ],
        default='monthly',
        verbose_name="نوع الاشتراك"
    )
    is_active = models.BooleanField(default=True, verbose_name="اشتراك فعال")
    
    # ===== ميزة تجميد الاشتراك =====
    is_frozen = models.BooleanField(default=False, verbose_name="اشتراك مجمد")
    frozen_start = models.DateField(null=True, blank=True, verbose_name="تاريخ بدء التجميد")
    frozen_end = models.DateField(null=True, blank=True, verbose_name="تاريخ انتهاء التجميد")
    frozen_days = models.IntegerField(default=0, verbose_name="عدد أيام التجميد")
    original_end = models.DateField(null=True, blank=True, verbose_name="تاريخ النهاية الأصلي")
    
    # ملاحظات
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    
    def days_until_expiry(self):
        """عدد الأيام المتبقية حتى انتهاء الاشتراك"""
        today = date.today()
        end_date = self.subscription_end
        if self.is_frozen and self.frozen_end and today <= self.frozen_end:
            # إذا كان مجمد، نحسب الأيام المتبقية من تاريخ انتهاء التجميد
            end_date = self.subscription_end
        if end_date >= today:
            return (end_date - today).days
        return 0
    
    def is_expired(self):
        """هل الاشتراك منتهي؟ (مع مراعاة التجميد)"""
        today = date.today()
        if self.is_frozen and self.frozen_end and today <= self.frozen_end:
            # إذا كان مجمد، الاشتراك ما زال ساري المفعول
            return False
        return today > self.subscription_end
    
    def get_actual_end_date(self):
        """تاريخ النهاية الفعلي بعد إضافة أيام التجميد"""
        if self.original_end:
            return self.original_end
        return self.subscription_end
    
    def freeze_subscription(self, days):
        """تجميد الاشتراك لعدد معين من الأيام"""
        today = date.today()
        self.is_frozen = True
        self.frozen_start = today
        self.frozen_end = today + timedelta(days=days)
        self.frozen_days = days
        self.original_end = self.subscription_end
        # تمديد تاريخ النهاية بعدد أيام التجميد
        self.subscription_end = self.subscription_end + timedelta(days=days)
        self.save()
        return True
    
    def unfreeze_subscription(self):
        """إلغاء التجميد"""
        self.is_frozen = False
        self.frozen_start = None
        self.frozen_end = None
        self.frozen_days = 0
        self.save()
        return True
    
    def __str__(self):
        return f"{self.name} - {self.subscription_end}"
    
    class Meta:
        verbose_name = "عضو"
        verbose_name_plural = "الأعضاء"
        ordering = ['-join_date']


class DailyAttendance(models.Model):
    """تسجيل الدخول اليومي"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendance')
    check_in_date = models.DateField(default=date.today, verbose_name="تاريخ الدخول")
    check_in_time = models.TimeField(auto_now_add=True, verbose_name="وقت الدخول")
    notes = models.CharField(max_length=100, blank=True, verbose_name="ملاحظات")
    
    class Meta:
        unique_together = ['member', 'check_in_date']
        verbose_name = "دخول يومي"
        verbose_name_plural = "الدخول اليومي"
        ordering = ['-check_in_date', '-check_in_time']
    
    def __str__(self):
        return f"{self.member.name} - {self.check_in_date}"