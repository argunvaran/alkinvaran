from django.shortcuts import render, redirect, get_object_or_404
from .models import HeroSection, Discipline, TrainingLevel, Studio, ContactMessage, AboutSection
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    hero = HeroSection.objects.first()
    about = AboutSection.objects.first()
    disciplines = Discipline.objects.all()
    levels = TrainingLevel.objects.all()
    studios = Studio.objects.all()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.')
        return redirect('index')

    context = {
        'hero': hero,
        'about': about,
        'disciplines': disciplines,
        'levels': levels,
        'studios': studios,
    }
    return render(request, 'website/index.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_message(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id)
    if request.method == 'POST':
        name = msg.full_name
        msg.delete()
        messages.success(request, f"{name} isimli kişinin mesajı başarıyla silindi.")
    return redirect('dashboard')

@user_passes_test(lambda u: u.is_superuser)
def manage_images(request):
    hero = HeroSection.objects.first()
    if not hero:
        hero = HeroSection.objects.create(title='POTANSİYELİNİ <span class="text-accent underline decoration-4">ŞEKİLLENDİR</span>', subtitle='Sınırlarını zorlayanlar için; fonksiyonel güç, modern hareket dinamikleri ve beden kontrolünü birleştiren elit antrenman programları. Sadece antrenman yapma, daha güçlü, esnek ve yenilmez bir bedene adım at.')
    
    about = AboutSection.objects.first()
    if not about:
        about = AboutSection.objects.create()
        
    disciplines = Discipline.objects.all()
    studios = Studio.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'hero':
            if 'hero_image' in request.FILES:
                hero.background_image = request.FILES['hero_image']
            hero.title = request.POST.get('title', hero.title)
            hero.subtitle = request.POST.get('subtitle', hero.subtitle)
            hero.button_text = request.POST.get('button_text', hero.button_text)
            hero.save()
            messages.success(request, 'Ana Sayfa (Hero) bilgileri başarıyla güncellendi.')
            
        elif action == 'about':
            if 'about_image' in request.FILES:
                about.portrait_image = request.FILES['about_image']
            about.title = request.POST.get('title', about.title)
            about.highlight_title = request.POST.get('highlight_title', about.highlight_title)
            about.content = request.POST.get('content', about.content)
            about.save()
            messages.success(request, 'Hakkımda bölümü başarıyla güncellendi.')
            
        elif action == 'discipline':
            disc_id = request.POST.get('discipline_id')
            if disc_id:
                disc = get_object_or_404(Discipline, id=disc_id)
                
                name = request.POST.get('name')
                description = request.POST.get('description')
                
                if name:
                    disc.name = name
                if description is not None:
                    disc.description = description
                    
                if 'discipline_image' in request.FILES:
                    disc.image = request.FILES['discipline_image']
                    
                disc.save()
                messages.success(request, f'"{disc.name}" disiplini başarıyla güncellendi.')
                
        elif action == 'studio':
            studio_id = request.POST.get('studio_id')
            if studio_id:
                studio = get_object_or_404(Studio, id=studio_id)
                name = request.POST.get('name')
                description = request.POST.get('description')
                location = request.POST.get('location')
                
                if name:
                    studio.name = name
                if description is not None:
                    studio.description = description
                if location is not None:
                    studio.location = location
                    
                if 'studio_image' in request.FILES:
                    studio.image = request.FILES['studio_image']
                    
                studio.save()
                messages.success(request, f'"{studio.name}" stüdyo kaydı başarıyla güncellendi.')
                
        return redirect('manage_images')

    context = {
        'hero': hero,
        'about': about,
        'disciplines': disciplines,
        'studios': studios,
    }
    return render(request, 'website/manage_images.html', context)
