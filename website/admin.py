from django.contrib import admin
from .models import HeroSection, Discipline, TrainingLevel, Studio, ContactMessage, AboutSection, BlogPost, AppNotification

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text')

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(TrainingLevel)
class TrainingLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'status_badge', 'created_at')
    list_display_links = ('id', 'full_name')
    list_filter = ('is_replied', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Danışan Bilgileri', {
            'fields': ('full_name', 'email', 'created_at')
        }),
        ('Mesaj Detayı', {
            'fields': ('subject', 'message')
        }),
        ('CRM Paneli (Yönetim)', {
            'fields': ('is_replied', 'admin_notes'),
            'description': 'Müşteriye dönüş yapıldığında buradan işaretleyebilir ve not alabilirsiniz.'
        })
    )

    def status_badge(self, obj):
        if obj.is_replied:
            return "✅ Dönüş Yapıldı"
        else:
            return "⏳ Bekliyor"
    status_badge.short_description = "Durum"

    actions = ['mark_as_replied']

    def mark_as_replied(self, request, queryset):
        updated = queryset.update(is_replied=True)
        self.message_user(request, f"{updated} mesaj 'Dönüş Yapıldı' olarak işaretlendi.")
    mark_as_replied.short_description = "Seçili mesajları 'Dönüş Yapıldı' işaretle"

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')

@admin.register(AppNotification)
class AppNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'device_id', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'device_id', 'message')
