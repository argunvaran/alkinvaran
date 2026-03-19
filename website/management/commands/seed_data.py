from django.core.management.base import BaseCommand
from website.models import HeroSection, Discipline, TrainingLevel, Studio
from django.core.files.base import ContentFile
import requests

class Command(BaseCommand):
    help = 'Seed initial data for the website'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Hero Section
        HeroSection.objects.get_or_create(
            title="MOULDING EXCELLENCE",
            subtitle="Disiplin, hareket ve estetiğin mükemmel uyumuyla potansiyelinizi yeniden keşfedin.",
            button_text="Şimdi Başlayın"
        )

        # Disciplines
        disciplines = [
            ("Handstand", "Dengenin ve gücün zirvesi."),
            ("Breakdance", "Ritim ve akrobasi bir arada."),
            ("Soft Acrobatics", "Esneklik ve akışkanlık."),
            ("Tumbling", "Dinamik patlayıcı güç.")
        ]
        for name, desc in disciplines:
            Discipline.objects.get_or_create(name=name, defaults={'description': desc})

        # Levels
        levels = [
            ('beg', 'Temel Seviye', 'Hareket dünyasına ilk adımınızı atın. Temel teknikler ve mobilite.'),
            ('int', 'Orta Seviye', 'Gücünüzü ve kontrolünüzü bir üst seviyeye taşıyın.'),
            ('adv', 'İleri Seviye', 'Sınırları zorlayın, uzmanlaşın.')
        ]
        for code, title, desc in levels:
            TrainingLevel.objects.get_or_create(name=code, defaults={'title': title, 'description': desc, 'icon_name': 'star'})

        # Studios
        studios = [
            ("Central Studio", "Maslak, Istanbul", "Modern ve geniş antrenman alanı."),
            ("Elite Gym", "Beşiktaş, Istanbul", "Kişiye özel çalışma imkanları.")
        ]
        for name, loc, desc in studios:
            Studio.objects.get_or_create(name=name, defaults={'location': loc, 'description': desc})

        self.stdout.write(self.style.SUCCESS('Successfully seeded data!'))
