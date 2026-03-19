from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('panel/images/', views.manage_images, name='manage_images'),
    ]
