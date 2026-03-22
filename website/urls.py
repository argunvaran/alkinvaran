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
    
    # API Routes for Mobile App
    path('api/v1/mobile/', views.mobile_api, name='mobile_api'),
    path('api/v1/mobile/blogs/', views.mobile_blogs_api, name='mobile_blogs_api'),
    path('api/v1/mobile/contact/', views.mobile_contact_api, name='mobile_contact_api'),
    path('api/v1/mobile/notifications/', views.mobile_notifications_api, name='mobile_notifications_api'),
    
    path('api/v1/mobile/admin/login/', views.mobile_admin_login),
    path('api/v1/mobile/admin/messages/', views.mobile_admin_messages),
    path('api/v1/mobile/admin/reply/', views.mobile_admin_reply),
    path('api/v1/mobile/admin/notify_all/', views.mobile_admin_notify_all),
    path('api/v1/mobile/admin/notify_selected/', views.mobile_admin_notify_selected),
    path('api/v1/mobile/admin/delete/', views.mobile_admin_delete),
]
