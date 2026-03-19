import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alkinvaran_proj.settings")
django.setup()

from website.models import BlogPost
from django.utils import timezone

posts_data = [
    {
        "title": "Cimnastik Temelleri: Neden Esneklikten Fazlasıdır?",
        "content": "<p>Cimnastik sadece esneklik değil, aynı zamanda bedeninizin farklı eksenlerde kuvvet uygulayabilme sanatıdır. Vücut ağırlığınızı ustalıkla kontrol etmeyi öğrendiğinizde, her hareket bir ustalık gösterisi haline gelir.</p><p><br></p><p>Core gücünün jimnastikteki yerine değinirsek, merkez bölgesinin stabilizasyonu hareketin tamamlanmasındaki yegane kilittir.</p>"
    },
    {
        "title": "Atletik Performansı Zirveye Taşıyan 5 Hata",
        "content": "<p>Sporcuların çoğu antrenman hacmini artırarak gelişeceklerini sanırlar. Ancak atletik performans, dinlenme kapasiteniz ve sinir sisteminizin uyarlanabilirliği ile ilgilidir.</p><p><br></p>Düşük hacimli dinlenmeler kas onarımını engelleyebilir. Uyku ve dinlenme döngülerinize saygı duymak gerçek performansı getirir."
    },
    {
        "title": "Handstand (Amut) İçin En Önemli Adım Ne?",
        "content": "<p>Herkes amuda kalkmak ister ama çok azı bilek mobilizasyonu ve omuz kuvvetinin önemini bilir. Amutta dengede kalmanın asıl sırrı düzgün bir hizalanmadır.</p><p><br></p>Omuzlarınızı kulaklarınıza doğru itmek (elevation) ağırlık merkezini doğru hizalar ve bel kavisini önler."
    },
    {
        "title": "Yetişkinlerde Hareket Kabiliyeti (Mobility) Neden Azalır?",
        "content": "<p>Saatlerce sandalyede oturmak kalça fleksörlerimizi kısaltır ve fasyamızı hareketsizliğe alıştırır. Mobility çalışmaları sadece sakatlıkları önlemekle kalmaz, performansınızı da katlar.</p>"
    },
    {
        "title": "Kişisel Eğitmenle (PT) Çalışmanın Fark Yaratan 3 Yönü",
        "content": "<p>Zaman çok değerlidir. Yanlış formla yapılan hareketler gelişiminizi yavaşlatır. Bir profesyonel sadece hareket saymaz; sizin kapasitenize uygun zorluk eşiklerini çizer.</p><br><p>İhtiyaca özel, tamamen hedefe kilitlenmiş bir antrenman programı size ayları hatta yılları geri kazandırır.</p>"
    },
    {
        "title": "Antrenman Öncesi Isınma Nasıl Olmalı?",
        "content": "<p>Klasik streçing ısınma değildir. Vücudun merkezi sinir sistemini aktif edecek, dinamik hareket geçişlerine ihtiyaç vardır. Jimnastikte kullandığımız bu protokollere göz atalım.</p>"
    },
    {
        "title": "Core (Merkez) Bölgesi Kuvveti Sadece Mekik Değildir",
        "content": "<p>Core bölgeniz hareketlerin enerjisini üst vücuda ve alt vücuda aktaran bir köprüdür. Hollow body hold ve plank varyasyonlarının neden mekikten bin kat daha etkili olduğunu keşfedin.</p>"
    },
    {
        "title": "Yeni Başlayanlar İçin Barfiks Rehberi",
        "content": "<p>Kendi kütlenizi yukarı çekmek, doğada hayatta kalmanın en temel donanımlarından biridir. Negatif tekrarlar ve direnç bandı çalışmalarıyla ilk nizami barfiksinizi nasıl çekeceğinizi öğreneceksiniz.</p>"
    },
    {
        "title": "Fonsiyonel Antrenman vs. Klasik Fitness Serbest Ağırlıklar",
        "content": "<p>İzole edilmiş makinelerde kasları büyütmek estetik olabilir, ancak fonksiyonel gücünüzü artırmaz. Jimnastik formlarıyla yapılan serbest ağırlık antrenmanları, her düzlemde sizi güçlendirir.</p>"
    },
    {
        "title": "Motivasyon Kaybı Yaşadığınızda Uygulamanız Gereken Protokol",
        "content": "<p>Disiplin, motivasyonun bittiği yerde başlar. Gelişim grafiğimiz hiçbir zaman sadece düz bir çizgi halinde yukarı çıkmaz. İniş ve çıkışları nasıl yöneteceğinizi konuşalım ve harekete sadık kalalım.</p>"
    }
]

# Start from around January 6, 2026.
current_date = datetime(2026, 1, 6, 11, 0, 0)
BlogPost.objects.all().delete()

for data in posts_data:
    post = BlogPost.objects.create(title=data['title'], content=data['content'])
    post.created_at = timezone.make_aware(current_date)
    post.save()
    
    # Move forward 6-9 days
    current_date += timedelta(days=random.randint(6, 9), hours=random.randint(1, 10))

print("10 Farklı tarihli blog yazısı başarıyla eklendi!")
