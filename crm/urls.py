from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='crm_login'),
    path('logout/', views.logout_view, name='crm_logout'),
    path('dashboard/', views.dashboard, name='crm_dashboard'),
    path('lessons/', views.lesson_list, name='crm_lesson_list'),
    path('lessons/add/', views.lesson_create, name='crm_lesson_create'),
    path('lessons/<int:lesson_id>/delete/', views.lesson_delete, name='crm_lesson_delete'),
    path('lessons/<int:lesson_id>/add_student/', views.lesson_add_student, name='crm_lesson_add_student'),
    path('lessons/<int:lesson_id>/remove_student/<int:student_id>/', views.lesson_remove_student, name='crm_lesson_remove_student'),
    path('students/', views.student_list, name='crm_student_list'),
    path('students/add/', views.student_create, name='crm_student_create'),
    path('students/<int:student_id>/delete/', views.student_delete, name='crm_student_delete'),
    path('payments/', views.payment_list, name='crm_payment_list'),
    path('payments/add/', views.payment_create, name='crm_payment_create'),
    path('payments/<int:payment_id>/delete/', views.payment_delete, name='crm_payment_delete'),
    path('finances/', views.net_status, name='crm_net_status'),
    path('finances/expense/add/', views.expense_create, name='crm_expense_create'),
    path('finances/expense/<int:expense_id>/delete/', views.expense_delete, name='crm_expense_delete'),
    path('inbox/', views.inbox, name='crm_inbox'),
    path('inbox/toggle/<int:msg_id>/', views.toggle_message_status, name='crm_toggle_message'),
    path('inbox/delete/<int:msg_id>/', views.delete_message, name='crm_delete_message'),
    path('', views.dashboard, name='crm_home'),
]
