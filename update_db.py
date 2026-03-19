import os
import django
import sys

# Ensure settings are configured if run as standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alkin.settings')
django.setup()

from website.models import HeroSection

hero = HeroSection.objects.first()
if hero:
    hero.title = 'POTANSİYELİNİ <span class="text-accent underline decoration-4">ŞEKİLLENDİR</span>'
    hero.subtitle = 'Sınırlarını zorlayanlar için; fonksiyonel güç, modern hareket dinamikleri ve beden kontrolünü birleştiren elit antrenman programları. Sadece antrenman yapma, daha güçlü, esnek ve yenilmez bir bedene adım at.'
    hero.save()
    print("Database updated!")
else:
    print("No hero found to update.")
