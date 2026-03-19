from django.contrib import admin
from .models import Student, Payment, Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'day_of_week', 'time')
    list_filter = ('day_of_week',)
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'status', 'registration_date')
    list_filter = ('status', 'registration_date')
    search_fields = ('full_name', 'phone', 'email')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('student__full_name', 'description')
