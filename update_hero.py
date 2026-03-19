import os, sys, django
sys.path.append('c:/Kutum/alkin')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alkinvaran_proj.settings')
django.setup()

from website.models import HeroSection

hero = HeroSection.objects.first()
if hero:
    print(f"Current Title: {hero.title}")
    hero.title = 'POTANSİYELİNİ <span class="text-accent underline decoration-4">ŞEKİLLENDİR</span>'
    hero.save()
    print("Hero updated.")
