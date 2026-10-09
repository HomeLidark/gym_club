from django import forms
from .models import Member
from datetime import datetime


class MemberForm(forms.ModelForm):
    # ===== حقول التاريخ مع التقويم =====
    subscription_start = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        label='بداية الاشتراك',
        input_formats=['%Y-%m-%d']
    )
    
    subscription_end = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        label='نهاية الاشتراك',
        input_formats=['%Y-%m-%d']
    )
    
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        label='تاريخ الميلاد',
        required=False,
        input_formats=['%Y-%m-%d']
    )
    
    class Meta:
        model = Member
        fields = [
            'name', 'phone', 'id_number', 'address', 'birth_date',
            'subscription_start', 'subscription_end', 'subscription_type',
            'is_active', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'subscription_type': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'الاسم',
            'phone': 'الهاتف',
            'id_number': 'رقم الهوية',
            'address': 'العنوان',
            'subscription_type': 'نوع الاشتراك',
            'is_active': 'اشتراك فعال',
            'notes': 'ملاحظات',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.birth_date:
                self.initial['birth_date'] = self.instance.birth_date.strftime('%Y-%m-%d')
            if self.instance.subscription_start:
                self.initial['subscription_start'] = self.instance.subscription_start.strftime('%Y-%m-%d')
            if self.instance.subscription_end:
                self.initial['subscription_end'] = self.instance.subscription_end.strftime('%Y-%m-%d')
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('subscription_start')
        end = cleaned_data.get('subscription_end')
        
        if start and end:
            if end < start:
                raise forms.ValidationError('⚠️ تاريخ نهاية الاشتراك يجب أن يكون بعد تاريخ البداية')
        
        return cleaned_data


# ===== نموذج تجميد الاشتراك =====
class FreezeForm(forms.Form):
    days = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'عدد أيام التجميد',
            'min': 1,
            'max': 365
        }),
        label='عدد أيام التجميد',
        min_value=1,
        max_value=365
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'سبب التجميد (اختياري)'
        }),
        label='سبب التجميد',
        required=False
    )


class AttendanceForm(forms.Form):
    member_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '🔍 أدخل رقم العضو',
            'autofocus': True
        }),
        label='رقم العضو'
    )