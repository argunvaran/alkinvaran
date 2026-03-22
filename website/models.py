from django.db import models
from django.utils.text import slugify
from django.core.files.base import ContentFile
from PIL import Image
import io
import os

def convert_to_webp(image_field, max_size=1920):
    if not image_field:
        return
    if image_field.name.lower().endswith('.webp'):
        return
    try:
        img = Image.open(image_field)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=85)
        output.seek(0)
        
        name = os.path.splitext(os.path.basename(image_field.name))[0] + '.webp'
        image_field.save(name, ContentFile(output.read()), save=False)
    except Exception as e:
        pass
class HeroSection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    subtitle = models.TextField(verbose_name="Alt Başlık")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL (Opsiyonel)")
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True, verbose_name="Arka Plan Görseli")
    button_text = models.CharField(max_length=50, default="Bize Ulaşın", verbose_name="Buton Metni")

    def save(self, *args, **kwargs):
        if self.background_image:
            convert_to_webp(self.background_image)
        super().save(*args, **kwargs)

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
    
    def save(self, *args, **kwargs):
        if self.portrait_image:
            convert_to_webp(self.portrait_image)
        super().save(*args, **kwargs)
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

    def save(self, *args, **kwargs):
        if self.image:
            convert_to_webp(self.image)
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if self.image:
            convert_to_webp(self.image)
        super().save(*args, **kwargs)

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
    device_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Gizli Cihaz Kimliği")
    
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

class AppNotification(models.Model):
    device_id = models.CharField(max_length=255, verbose_name="Gizli Cihaz Kimliği")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    message = models.TextField(verbose_name="Bildirim İçeriği")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")
    
    def __str__(self):
        return f"Bildirim: {self.title} -> {self.device_id[:8]}"
        
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Uygulama İçi Bildirim"
        verbose_name_plural = "Uygulama İçi Bildirimler"

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="SEO URL (Otomatik Dolur)")
    content = models.TextField(verbose_name="Metin/İçerik")
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Kapak Görseli")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yazılma Tarihi")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.image:
            convert_to_webp(self.image)
        super().save(*args, **kwargs)

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        DEFAULT_IMAGES = [
            "/media/blog_defaults/1.webp",
            "/media/blog_defaults/2.webp",
            "/media/blog_defaults/5.webp",
        ]
        index = (self.id if self.id else len(self.slug)) % len(DEFAULT_IMAGES)
        return DEFAULT_IMAGES[index]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"
