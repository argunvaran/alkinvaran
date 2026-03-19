from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('panel/images/', views.manage_images, name='manage_images'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # CRM Edit Routes
    path('panel/blog/', views.crm_blog_list, name='crm_blog_list'),
    path('panel/blog/yeni/', views.crm_blog_create, name='crm_blog_create'),
    path('panel/blog/duzenle/<int:pk>/', views.crm_blog_update, name='crm_blog_update'),
    path('panel/blog/sil/<int:pk>/', views.crm_blog_delete, name='crm_blog_delete'),
    path('panel/blog/yayinla-siradaki/', views.crm_blog_publish_next, name='crm_blog_publish_next'),
]
