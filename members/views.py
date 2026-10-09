from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Count
from django.http import JsonResponse
from datetime import date, timedelta
from calendar import monthrange
from .models import Member, DailyAttendance
from .forms import MemberForm, AttendanceForm, FreezeForm


# ========== تسجيل الدخول ==========
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, '❌ اسم المستخدم أو كلمة المرور غير صحيحة')
    return render(request, 'members/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ========== لوحة التحكم ==========
@login_required
def dashboard(request):
    today = date.today()
    
    # ===== الإحصائيات =====
    total_members = Member.objects.count()
    
    # الأعضاء النشطين (غير مجمدين وغير منتهي اشتراكهم)
    active_members = Member.objects.filter(
        is_active=True, 
        subscription_end__gte=today, 
        is_frozen=False
    ).count()
    
    # الأعضاء المجمدين
    frozen_members = Member.objects.filter(
        is_frozen=True
    ).count()
    
    # الأعضاء المنتهي اشتراكهم
    expired_members = Member.objects.filter(
        subscription_end__lt=today
    ).count()
    
    # الأعضاء النشطين + المجمدين (اللي اشتراكهم ساري)
    total_active = Member.objects.filter(
        is_active=True,
        subscription_end__gte=today
    ).count()
    
    # الأعضاء على وشك الانتهاء (خلال 7 أيام)
    expiring_soon = Member.objects.filter(
        subscription_end__gte=today,
        subscription_end__lte=today + timedelta(days=7),
        is_frozen=False
    ).order_by('subscription_end')
    
    # دخول اليوم
    today_attendance = DailyAttendance.objects.filter(check_in_date=today)
    today_count = today_attendance.count()
    
    # آخر 10 عمليات دخول
    recent_attendance = DailyAttendance.objects.order_by('-check_in_date', '-check_in_time')[:10]
    
    context = {
        'total_members': total_members,
        'active_members': active_members,
        'frozen_members': frozen_members,
        'expired_members': expired_members,
        'total_active': total_active,
        'expiring_soon': expiring_soon,
        'today_count': today_count,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'members/dashboard.html', context)


# ========== إدارة الأعضاء ==========
@login_required
def member_list(request):
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    members = Member.objects.all().order_by('-join_date')
    
    if search:
        members = members.filter(
            Q(name__icontains=search) | 
            Q(phone__icontains=search) | 
            Q(id_number__icontains=search)
        )
    
    if status == 'active':
        members = members.filter(is_active=True, subscription_end__gte=date.today(), is_frozen=False)
    elif status == 'frozen':
        members = members.filter(is_frozen=True)
    elif status == 'expired':
        members = members.filter(subscription_end__lt=date.today())
    elif status == 'expiring':
        members = members.filter(
            subscription_end__gte=date.today(),
            subscription_end__lte=date.today() + timedelta(days=7),
            is_frozen=False
        )
    
    # ===== حساب الإحصائيات =====
    total_count = members.count()
    active_count = members.filter(is_active=True, is_frozen=False, subscription_end__gte=date.today()).count()
    frozen_count = members.filter(is_frozen=True).count()
    expired_count = members.filter(subscription_end__lt=date.today()).count()
    
    context = {
        'members': members,
        'total_count': total_count,
        'active_count': active_count,
        'frozen_count': frozen_count,
        'expired_count': expired_count,
    }
    return render(request, 'members/member_list.html', context)

@login_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'✅ تم إضافة العضو {member.name} بنجاح')
            return redirect('member_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {field}: {error}')
    else:
        form = MemberForm()
    
    return render(request, 'members/member_form.html', {'form': form, 'title': 'إضافة عضو جديد'})


@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ تم تحديث بيانات {member.name} بنجاح')
            return redirect('member_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {field}: {error}')
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/member_form.html', {'form': form, 'title': 'تعديل بيانات العضو'})


@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        name = member.name
        member.delete()
        messages.success(request, f'✅ تم حذف العضو {name} بنجاح')
        return redirect('member_list')
    return render(request, 'members/delete_confirm.html', {'member': member})


# ========== تسجيل الدخول اليومي ==========
@login_required
def attendance(request):
    today = date.today()
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data['member_id']
            try:
                member = Member.objects.get(id=member_id)
                
                if member.subscription_end < today:
                    messages.error(request, f'⚠️ اشتراك {member.name} منتهي!')
                    return redirect('attendance')
                
                if member.is_frozen:
                    messages.error(request, f'⚠️ اشتراك {member.name} مجمد حالياً!')
                    return redirect('attendance')
                
                if DailyAttendance.objects.filter(member=member, check_in_date=today).exists():
                    messages.warning(request, f'⚠️ {member.name} مسجل دخول اليوم بالفعل')
                    return redirect('attendance')
                
                DailyAttendance.objects.create(member=member)
                messages.success(request, f'✅ تم تسجيل دخول {member.name}')
                return redirect('attendance')
            except Member.DoesNotExist:
                messages.error(request, '❌ العضو غير موجود')
                return redirect('attendance')
        else:
            messages.error(request, '❌ الرجاء إدخال رقم عضو صحيح')
    else:
        form = AttendanceForm()
    
    today_attendance = DailyAttendance.objects.filter(
        check_in_date=today
    ).select_related('member')
    
    active_members = Member.objects.filter(
        is_active=True,
        subscription_end__gte=today,
        is_frozen=False
    ).exclude(
        id__in=today_attendance.values_list('member_id', flat=True)
    ).order_by('name')
    
    total_active = Member.objects.filter(
        is_active=True,
        subscription_end__gte=today,
        is_frozen=False
    ).count()
    
    context = {
        'form': form,
        'today': today,
        'today_attendance': today_attendance,
        'active_members': active_members,
        'total_active': total_active,
    }
    return render(request, 'members/attendance.html', context)


# ========== تجميد وإلغاء تجميد الاشتراك ==========
@login_required
def freeze_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    
    # التحقق من أن العضو غير مجمد بالفعل
    if member.is_frozen:
        messages.warning(request, f'⚠️ اشتراك {member.name} مجمد بالفعل!')
        return redirect('member_list')
    
    # التحقق من أن العضو نشط
    if member.is_expired():
        messages.error(request, f'⚠️ اشتراك {member.name} منتهي، لا يمكن تجميده!')
        return redirect('member_list')
    
    if request.method == 'POST':
        form = FreezeForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['days']
            notes = form.cleaned_data.get('notes', '')
            
            # تجميد الاشتراك
            member.freeze_subscription(days)
            
            # إضافة ملاحظة
            if notes:
                current_notes = member.notes or ''
                member.notes = f"{current_notes}\n[{date.today()}] تم تجميد الاشتراك لمدة {days} يوم - {notes}" if current_notes else f"[{date.today()}] تم تجميد الاشتراك لمدة {days} يوم - {notes}"
                member.save()
            
            messages.success(request, f'✅ تم تجميد اشتراك {member.name} لمدة {days} يوم')
            return redirect('member_list')
    else:
        form = FreezeForm()
    
    return render(request, 'members/freeze_member.html', {
        'form': form,
        'member': member
    })


@login_required
def unfreeze_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    
    if not member.is_frozen:
        messages.warning(request, f'⚠️ اشتراك {member.name} غير مجمد!')
        return redirect('member_list')
    
    if request.method == 'POST':
        # إلغاء التجميد
        member.unfreeze_subscription()
        
        # إضافة ملاحظة
        current_notes = member.notes or ''
        member.notes = f"{current_notes}\n[{date.today()}] تم إلغاء تجميد الاشتراك" if current_notes else f"[{date.today()}] تم إلغاء تجميد الاشتراك"
        member.save()
        
        messages.success(request, f'✅ تم إلغاء تجميد اشتراك {member.name}')
        return redirect('member_list')
    
    return render(request, 'members/unfreeze_member.html', {'member': member})


# ========== تقرير الحضور الشهري ==========
@login_required
def monthly_report(request):
    today = date.today()
    
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if month and year:
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            month = today.month
            year = today.year
    else:
        month = today.month
        year = today.year
    
    days_in_month = monthrange(year, month)[1]
    
    month_start = date(year, month, 1)
    month_end = date(year, month, days_in_month)
    
    members = Member.objects.filter(
        is_active=True
    ).order_by('name')
    
    report_data = []
    for member in members:
        attendance_count = DailyAttendance.objects.filter(
            member=member,
            check_in_date__gte=month_start,
            check_in_date__lte=month_end
        ).count()
        
        report_data.append({
            'member': member,
            'attendance_count': attendance_count,
            'days_in_month': days_in_month,
        })
    
    report_data.sort(key=lambda x: x['attendance_count'], reverse=True)
    
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    context = {
        'report_data': report_data,
        'month': month,
        'year': year,
        'month_name': month_start.strftime('%B'),
        'month_start': month_start,
        'month_end': month_end,
        'days_in_month': days_in_month,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'total_members': members.count(),
    }
    return render(request, 'members/monthly_report.html', context)


# ========== تنبيهات التجديد ==========
@login_required
def renewal_alerts(request):
    today = date.today()
    
    expired = Member.objects.filter(subscription_end__lt=today).order_by('subscription_end')
    expiring_soon = Member.objects.filter(
        subscription_end__gte=today,
        subscription_end__lte=today + timedelta(days=7),
        is_frozen=False
    ).order_by('subscription_end')
    expiring_later = Member.objects.filter(
        subscription_end__gt=today + timedelta(days=7),
        subscription_end__lte=today + timedelta(days=14),
        is_frozen=False
    ).order_by('subscription_end')
    
    context = {
        'expired': expired,
        'expiring_soon': expiring_soon,
        'expiring_later': expiring_later,
    }
    return render(request, 'members/renewal_alerts.html', context)


@login_required
def alert_count(request):
    today = date.today()
    count = Member.objects.filter(
        subscription_end__gte=today,
        subscription_end__lte=today + timedelta(days=7),
        is_frozen=False
    ).count()
    return JsonResponse({'count': count})


# ========== التقارير ==========
@login_required
def reports(request):
    today = date.today()
    month_start = today.replace(day=1)
    
    monthly_attendance = DailyAttendance.objects.filter(
        check_in_date__gte=month_start
    ).count()
    
    top_members = DailyAttendance.objects.values('member__name').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'monthly_attendance': monthly_attendance,
        'top_members': top_members,
    }
    return render(request, 'members/reports.html', context)