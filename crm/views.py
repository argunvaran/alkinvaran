from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Student, Payment, Lesson, Expense
from website.models import ContactMessage
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime

def login_view(request):
    if request.user.is_authenticated:
        return redirect('crm_dashboard')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect('crm_dashboard')
        else:
            messages.error(request, "Giriş bilgileri hatalı veya yetkiniz yok.")
            
    return render(request, 'crm/login.html')

@login_required(login_url='crm_login')
def logout_view(request):
    auth_logout(request)
    return redirect('crm_login')

@login_required(login_url='crm_login')
def dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    total_lessons = Lesson.objects.count()
    total_revenue = Payment.objects.aggregate(t=Sum('amount'))['t'] or 0

    messages_qs = ContactMessage.objects.filter(is_replied=False).order_by('-created_at')
    payments_qs = Payment.objects.all().order_by('-payment_date')

    if request.GET.get('load_messages'):
        paginator = Paginator(messages_qs, 5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'crm/partials/_dash_messages.html', {'recent_messages': page_obj.object_list, 'messages_page': page_obj})

    if request.GET.get('load_payments'):
        paginator = Paginator(payments_qs, 5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'crm/partials/_dash_payments.html', {'recent_payments': page_obj.object_list, 'payments_page': page_obj})

    msg_paginator = Paginator(messages_qs, 5)
    messages_page = msg_paginator.get_page(1)
    
    pay_paginator = Paginator(payments_qs, 5)
    payments_page = pay_paginator.get_page(1)

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'total_lessons': total_lessons,
        'total_revenue': total_revenue,
        'recent_messages': messages_page.object_list,
        'messages_page': messages_page,
        'recent_payments': payments_page.object_list,
        'payments_page': payments_page,
    }
    return render(request, 'crm/dashboard.html', context)


@login_required(login_url='crm_login')
def student_list(request):
    qs = Student.objects.all()
    q = request.GET.get('q')
    if q:
        qs = qs.filter(full_name__icontains=q)
        
    context = {'students': qs}
    return render(request, 'crm/student_list.html', context)
    
@login_required(login_url='crm_login')
def payment_list(request):
    lessons = Lesson.objects.all()
    selected_lesson_id = request.GET.get('lesson_id')
    payment_status_filter = request.GET.get('payment_status', 'all')
    
    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))
    
    context = {
        'lessons': lessons,
        'selected_lesson_id': int(selected_lesson_id) if selected_lesson_id else None,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'payment_status_filter': payment_status_filter,
        'months': Payment.MONTH_CHOICES,
        'years': [now.year - 1, now.year, now.year + 1],
    }
    
    if selected_lesson_id:
        lesson = get_object_or_404(Lesson, id=selected_lesson_id)
        students = lesson.students.filter(status='active').order_by('full_name')
        
        # Get payments for this lesson, month, year
        payments = Payment.objects.filter(lesson=lesson, payment_month=selected_month, payment_year=selected_year)
        payment_dict = {p.student_id: p for p in payments}
        
        student_data = []
        for s in students:
            student_data.append({
                'student': s,
                'payment': payment_dict.get(s.id)
            })
            
        context['student_data'] = student_data
        context['selected_lesson'] = lesson
    else:
        lesson_stats = []
        for lesson in lessons:
            active_students = lesson.students.filter(status='active').count()
            if active_students == 0:
                continue
                
            payments = Payment.objects.filter(lesson=lesson, payment_month=selected_month, payment_year=selected_year)
            paid_count = payments.values('student_id').distinct().count()
            total_amount = payments.aggregate(t=Sum('amount'))['t'] or 0
            
            has_any_payment = paid_count > 0
            is_fully_paid = paid_count >= active_students
            
            if payment_status_filter == 'paid' and not has_any_payment:
                continue
            if payment_status_filter == 'unpaid' and is_fully_paid:
                continue
                
            lesson_stats.append({
                'lesson': lesson,
                'active_students': active_students,
                'paid_count': paid_count,
                'total_amount': total_amount,
                'progress_percentage': int((paid_count / active_students * 100)) if active_students > 0 else 0
            })
            
        context['lesson_stats'] = lesson_stats
        
    return render(request, 'crm/payment_list.html', context)

@login_required(login_url='crm_login')
def payment_create(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        student_id = request.POST.get('student_id')
        lesson_id = request.POST.get('lesson_id')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method', 'transfer')
        payment_month = request.POST.get('payment_month')
        payment_year = request.POST.get('payment_year')
        
        if student_id and lesson_id and amount:
            if payment_id:
                payment = get_object_or_404(Payment, id=payment_id)
                payment.amount = amount
                payment.payment_method = payment_method
                payment.save()
                messages.success(request, "Ödeme başarıyla güncellendi.")
            else:
                Payment.objects.create(
                    student_id=student_id,
                    lesson_id=lesson_id,
                    amount=amount,
                    payment_method=payment_method,
                    payment_month=payment_month,
                    payment_year=payment_year,
                    payment_date=timezone.now().date(),
                    description=f"{dict(Payment.MONTH_CHOICES).get(int(payment_month), '')} {payment_year} Aidatı"
                )
                messages.success(request, "Ödeme başarıyla kaydedildi.")
        else:
            messages.error(request, "Lütfen gerekli bilgileri doldurun.")
            
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('crm_payment_list')

@login_required(login_url='crm_login')
def payment_delete(request, payment_id):
    if request.method == 'POST':
        payment = get_object_or_404(Payment, id=payment_id)
        payment.delete()
        messages.success(request, "Ödeme kaydı iptal edildi (Ödenmedi durumuna çekildi).")
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('crm_payment_list')

@login_required(login_url='crm_login')
def lesson_list(request):
    qs = Lesson.objects.all().prefetch_related('students')
    all_students = Student.objects.filter(status='active').order_by('full_name')
    context = {'lessons': qs, 'all_students': all_students}
    return render(request, 'crm/lesson_list.html', context)

@login_required(login_url='crm_login')
def lesson_create(request):
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        name = request.POST.get('name')
        day_of_week = request.POST.get('day_of_week')
        time = request.POST.get('time')
        notes = request.POST.get('notes')
        
        if name and day_of_week and time:
            if lesson_id:
                lesson = get_object_or_404(Lesson, id=lesson_id)
                lesson.name = name
                lesson.day_of_week = day_of_week
                lesson.time = time
                lesson.notes = notes
                lesson.save()
                messages.success(request, f"{name} dersi güncellendi.")
            else:
                Lesson.objects.create(name=name, day_of_week=day_of_week, time=time, notes=notes)
                messages.success(request, f"{name} dersi başarıyla eklendi.")
        else:
            messages.error(request, "Lütfen gerekli ders alanlarını doldurun.")
    return redirect('crm_lesson_list')

@login_required(login_url='crm_login')
def lesson_add_student(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        student_id = request.POST.get('student_id')
        new_student_name = request.POST.get('new_student_name')
        
        if student_id and student_id != 'new':
            # Add existing student
            student = get_object_or_404(Student, id=student_id)
            student.lessons.add(lesson)
            messages.success(request, f"{student.full_name}, {lesson.name} dersine eklendi.")
        elif new_student_name:
            # Create new student and add
            new_phone = request.POST.get('new_student_phone', '')
            student = Student.objects.create(full_name=new_student_name, phone=new_phone, status='active')
            student.lessons.add(lesson)
            messages.success(request, f"Yeni öğrenci {student.full_name} oluşturuldu ve {lesson.name} dersine eklendi.")
        else:
            messages.error(request, "Lütfen eklenecek bir öğrenci seçin veya yeni öğrenci adı girin.")
            
    return redirect('crm_lesson_list')

@login_required(login_url='crm_login')
def student_create(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        notes = request.POST.get('notes')
        status = request.POST.get('status', 'active')
        
        if full_name:
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                    student.full_name = full_name
                    student.phone = phone
                    student.email = email
                    student.notes = notes
                    student.status = status
                    student.save()
                    messages.success(request, f"{full_name} isimli öğrenci güncellendi.")
                except Student.DoesNotExist:
                    messages.error(request, "Öğrenci bulunamadı.")
            else:
                Student.objects.create(full_name=full_name, phone=phone, email=email, notes=notes, status=status)
                messages.success(request, f"{full_name} isimli öğrenci eklendi.")
        else:
            messages.error(request, "Öğrenci adı zorunludur.")
    return redirect('crm_student_list')

@login_required(login_url='crm_login')
def net_status(request):
    now = datetime.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))
    
    # Calculate incomes
    payments = Payment.objects.filter(payment_month=selected_month, payment_year=selected_year)
    total_income = payments.aggregate(t=Sum('amount'))['t'] or 0
    
    # Get and calculate expenses
    expenses = Expense.objects.filter(expense_month=selected_month, expense_year=selected_year).order_by('-date')
    total_expense = expenses.aggregate(t=Sum('amount'))['t'] or 0
    
    net_profit = total_income - total_expense
    
    context = {
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': Payment.MONTH_CHOICES,
        'years': [now.year - 1, now.year, now.year + 1],
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': net_profit,
        'expenses': expenses,
        'expense_categories': Expense.EXPENSE_CATEGORIES,
    }
    return render(request, 'crm/net_status.html', context)

@login_required(login_url='crm_login')
def expense_create(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        description = request.POST.get('description')
        expense_month = request.POST.get('expense_month')
        expense_year = request.POST.get('expense_year')
        
        if amount and description:
            Expense.objects.create(
                amount=amount,
                category=category,
                description=description,
                expense_month=expense_month,
                expense_year=expense_year,
                date=timezone.now().date(),
            )
            messages.success(request, "Gider başarıyla eklendi.")
        else:
            messages.error(request, "Lütfen gerekli bilgileri doldurun.")
            
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('crm_net_status')

@login_required(login_url='crm_login')
def expense_delete(request, expense_id):
    if request.method == 'POST':
        expense = get_object_or_404(Expense, id=expense_id)
        expense.delete()
        messages.success(request, "Gider kaydı silindi.")
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('crm_net_status')

@login_required(login_url='crm_login')
def lesson_delete(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson_name = lesson.name
        lesson.delete()
        messages.success(request, f"{lesson_name} dersi başarıyla silindi.")
    return redirect('crm_lesson_list')

@login_required(login_url='crm_login')
def lesson_remove_student(request, lesson_id, student_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        student = get_object_or_404(Student, id=student_id)
        student.lessons.remove(lesson)
        messages.success(request, f"{student.full_name}, {lesson.name} dersinden çıkarıldı.")
    return redirect('crm_lesson_list')

@login_required(login_url='crm_login')
def student_delete(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student_name = student.full_name
        student.delete()
        messages.success(request, f"{student_name} başarıyla silindi.")
    return redirect('crm_student_list')


@login_required(login_url='crm_login')
def inbox(request):
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    
    # Simple statistics
    total_messages = contact_messages.count()
    replied_messages = contact_messages.filter(is_replied=True).count()
    pending_messages = total_messages - replied_messages
    
    # 1. Search Functionality
    q = request.GET.get('q', '').strip()
    if q:
        contact_messages = contact_messages.filter(
            Q(full_name__icontains=q) | 
            Q(email__icontains=q) | 
            Q(subject__icontains=q) | 
            Q(message__icontains=q)
        )
        
    # 2. Filter Functionality
    status = request.GET.get('status', 'all')
    if status == 'pending':
        contact_messages = contact_messages.filter(is_replied=False)
    elif status == 'replied':
        contact_messages = contact_messages.filter(is_replied=True)
        
    # 3. Lazy Load / Pagination Functionality
    paginator = Paginator(contact_messages, 5) # 5 messages per page for lazy loading demonstration
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'messages': page_obj.object_list,
        'page_obj': page_obj,
        'total_messages': total_messages,
        'replied_messages': replied_messages,
        'pending_messages': pending_messages,
        'q': q,
        'status': status,
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'crm/partials/_messages_list.html', context)
        
    return render(request, 'crm/inbox.html', context)

@login_required(login_url='crm_login')
def toggle_message_status(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id)
    msg.is_replied = not msg.is_replied
    msg.save()
    if msg.is_replied:
        messages.success(request, f"{msg.full_name} isimli kişinin mesajı 'Dönüş Yapıldı' olarak işaretlendi.")
    else:
        messages.warning(request, f"{msg.full_name} isimli kişinin mesajı 'Bekliyor' olarak değiştirildi.")
    return redirect('crm_inbox')

@login_required(login_url='crm_login')
def delete_message(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id)
    if request.method == 'POST':
        name = msg.full_name
        msg.delete()
        messages.success(request, f"{name} isimli kişinin mesajı başarıyla silindi.")
    return redirect('crm_inbox')
