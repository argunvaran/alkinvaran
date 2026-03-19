from django.db import models

class HeroSection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    subtitle = models.TextField(verbose_name="Alt Başlık")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL (Opsiyonel)")
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True, verbose_name="Arka Plan Görseli")
    button_text = models.CharField(max_length=50, default="Bize Ulaşın", verbose_name="Buton Metni")

    @property
    def has_image(self):
        return bool(self.background_image and self.background_image.storage.exists(self.background_image.name))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Hero Bölümü"
        verbose_name_plural = "Hero Bölümü"

class AboutSection(models.Model):
    title = models.CharField(max_length=100, default="Hareketin", verbose_name="Ana Başlık")
    highlight_title = models.CharField(max_length=100, default="Mimarisi", verbose_name="Vurgulu Başlık")
    content = models.TextField(default="Ben Alkin Varan...", verbose_name="Hakkımda İçeriği")
    portrait_image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Hakkımda Profil Görseli")
    
    @property
    def has_image(self):
        return bool(self.portrait_image and self.portrait_image.storage.exists(self.portrait_image.name))

    class Meta:
        verbose_name = "Hakkımda Bölümü"
        verbose_name_plural = "Hakkımda Bölümü"

class Discipline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Disiplin Adı")
    description = models.TextField(verbose_name="Açıklama")
    image = models.ImageField(upload_to='disciplines/', blank=True, null=True, verbose_name="Görsel")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")

    @property
    def has_image(self):
        return bool(self.image and self.image.storage.exists(self.image.name))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Disiplin"
        verbose_name_plural = "Disiplinler"

class TrainingLevel(models.Model):
    LEVEL_CHOICES = [
        ('beg', 'Başlangıç'),
        ('int', 'Orta'),
        ('adv', 'İleri'),
    ]
    name = models.CharField(max_length=50, choices=LEVEL_CHOICES, verbose_name="Seviye")
    title = models.CharField(max_length=100, verbose_name="Seviye Başlığı")
    description = models.TextField(verbose_name="Açıklama")
    icon_name = models.CharField(max_length=50, help_text="Lucide icon name or emoji", verbose_name="İkon")

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Eğitim Seviyesi"
        verbose_name_plural = "Eğitim Seviyeleri"

class Studio(models.Model):
    name = models.CharField(max_length=100, verbose_name="Stüdyo Adı")
    location = models.CharField(max_length=255, verbose_name="Konum")
    description = models.TextField(verbose_name="Açıklama")
    image = models.ImageField(upload_to='studios/', blank=True, null=True, verbose_name="Görsel")
    instagram_link = models.URLField(blank=True, null=True, verbose_name="Instagram Linki")
    map_link = models.URLField(blank=True, null=True, verbose_name="Google Harita Linki")

    @property
    def has_image(self):
        return bool(self.image and self.image.storage.exists(self.image.name))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Stüdyo"
        verbose_name_plural = "Stüdyolar"

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon Numarası")
    subject = models.CharField(max_length=200, verbose_name="Konu")
    message = models.TextField(verbose_name="Mesaj")
    
    # CRM Tracking functionality
    is_replied = models.BooleanField(default=False, verbose_name="Dönüş Yapıldı")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Yönetici Notları (Sadece siz görürsünüz)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Tarihi")

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Danışan/İletişim Mesajı"
        verbose_name_plural = "Gelen Kutusu (CRM)"
