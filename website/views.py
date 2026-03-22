from django.shortcuts import render, redirect, get_object_or_404
from .models import HeroSection, Discipline, TrainingLevel, Studio, ContactMessage, AboutSection, BlogPost
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

def blog_list(request):
    from django.utils import timezone
    from django.db.models import Q
    query = request.GET.get('q', '')
    posts_list = BlogPost.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')
    
    if query:
        posts_list = posts_list.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
    paginator = Paginator(posts_list, 6) # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'website/blog_list.html', {'page_obj': page_obj, 'query': query})

def blog_detail(request, slug):
    from django.utils import timezone
    post = get_object_or_404(BlogPost, slug=slug, created_at__lte=timezone.now())
    # Get 3 recent posts excluding the current one
    recent_posts = BlogPost.objects.filter(created_at__lte=timezone.now()).exclude(id=post.id).order_by('-created_at')[:3]
    return render(request, 'website/blog_detail.html', {'post': post, 'recent_posts': recent_posts})

# --- CRM Blog Yönetimi Yönlendirmeleri ---

@user_passes_test(lambda u: u.is_superuser)
def crm_blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'website/crm_blog_list.html', {'posts': posts})

@user_passes_test(lambda u: u.is_superuser)
def crm_blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        BlogPost.objects.create(title=title, content=content, image=image)
        messages.success(request, f'"{title}" başarıyla eklendi!')
        return redirect('crm_blog_list')
    return render(request, 'website/crm_blog_form.html', {'title': 'Yeni Yazı Ekle'})

@user_passes_test(lambda u: u.is_superuser)
def crm_blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if 'image' in request.FILES:
            post.image = request.FILES.get('image')
        post.save()
        messages.success(request, f'"{post.title}" başarıyla güncellendi!')
        return redirect('crm_blog_list')
    return render(request, 'website/crm_blog_form.html', {'post': post, 'title': 'Yazıyı Düzenle'})

@user_passes_test(lambda u: u.is_superuser)
def crm_blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'"{title}" yazısı başarıyla silindi.')
    return redirect('crm_blog_list')

@user_passes_test(lambda u: u.is_superuser)
def crm_blog_publish_next(request):
    from django.utils import timezone
    if request.method == 'POST':
        # Find the earliest scheduled post that hasn't been published yet
        next_post = BlogPost.objects.filter(created_at__gt=timezone.now()).order_by('created_at').first()
        if next_post:
            next_post.created_at = timezone.now()
            next_post.save()
            messages.success(request, f'Sıradaki bekleyen yazı olan "{next_post.title}" başarıyla şu an yayınlandı!')
        else:
            messages.warning(request, 'Sırada bekleyen (zamanlanmış) herhangi bir yazı bulunmuyor.')
    return redirect('crm_blog_list')

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def mobile_api(request):
    try:
        studios = list(Studio.objects.all().values('id', 'name', 'location', 'description', 'image', 'instagram_link', 'map_link'))
        levels = list(TrainingLevel.objects.all().values('id', 'name', 'title', 'description', 'icon_name'))
        disciplines = list(Discipline.objects.all().values('id', 'name', 'description', 'image', 'order'))
        about_query = AboutSection.objects.values('title', 'highlight_title', 'content', 'portrait_image').first()
        hero_query = HeroSection.objects.values('title', 'subtitle', 'button_text', 'background_image').first()
        
        # Helper to safely construct full URLs
        def build_url(path):
            if path:
                return request.build_absolute_uri('/media/' + path)
            return None

        # Fix media URLs if they exist
        for s in studios:
            s['image'] = build_url(s.get('image'))
        for d in disciplines:
            d['image'] = build_url(d.get('image'))
            
        about = None
        if about_query:
            about = {
                'title': about_query.get('title'),
                'highlight_title': about_query.get('highlight_title'),
                'content': about_query.get('content'),
                'portrait_image': build_url(about_query.get('portrait_image'))
            }

        hero = None
        if hero_query:
            hero = {
                'title': hero_query.get('title'),
                'subtitle': hero_query.get('subtitle'),
                'button_text': hero_query.get('button_text'),
                'background_image': build_url(hero_query.get('background_image'))
            }

        from django.utils import timezone
        blogs_qs = BlogPost.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')[:4]
        blogs = []
        for b in blogs_qs:
            image_url = b.display_image_url
            if image_url.startswith('/'):
                image_url = request.build_absolute_uri(image_url)
            blogs.append({
                'id': b.id,
                'title': b.title,
                'slug': b.slug,
                'excerpt': b.content[:120] + '...' if len(b.content) > 120 else b.content,
                'content': b.content,
                'image': image_url,
                'created_at': b.created_at.strftime('%d.%m.%Y')
            })

        return JsonResponse({
            'success': True,
            'hero': hero,
            'studios': studios,
            'levels': levels,
            'disciplines': disciplines,
            'about': about,
            'blogs': blogs,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def mobile_blogs_api(request):
    try:
        from django.utils import timezone
        query = request.GET.get('q', '')
        page = int(request.GET.get('page', 1))
        
        blogs_qs = BlogPost.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')
        if query:
            blogs_qs = blogs_qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
            
        paginator = Paginator(blogs_qs, 10) # Sayfa kasmaması için limitli
        page_obj = paginator.get_page(page)
        
        blogs = []
        for b in page_obj:
            image_url = b.display_image_url
            if image_url.startswith('/'):
                image_url = request.build_absolute_uri(image_url)
                
            blogs.append({
                'id': b.id,
                'title': b.title,
                'slug': b.slug,
                'excerpt': b.content[:150] + '...' if len(b.content) > 150 else b.content,
                'content': b.content,
                'image': image_url,
                'created_at': b.created_at.strftime('%d.%m.%Y')
            })
            
        return JsonResponse({
            'success': True,
            'blogs': blogs,
            'has_next': page_obj.has_next(),
            'total_pages': paginator.num_pages
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def mobile_contact_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            email = data.get('email')
            phone = data.get('phone', '')
            subject = data.get('subject')
            message = data.get('message')
            device_id = data.get('device_id', '')
            
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                device_id=device_id
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

@csrf_exempt
def mobile_notifications_api(request):
    try:
        from .models import AppNotification
        if request.method == 'POST':
            # Mark as read
            data = json.loads(request.body) if request.body else {}
            device_id = data.get('device_id')
            if device_id:
                AppNotification.objects.filter(device_id=device_id, is_read=False).update(is_read=True)
            return JsonResponse({'success': True})
            
        # GET request
        device_id = request.GET.get('device_id')
        if not device_id:
            return JsonResponse({'success': False, 'error': 'No device id'})
            
        notifs = AppNotification.objects.filter(device_id=device_id)[:15]
        unread = AppNotification.objects.filter(device_id=device_id, is_read=False).count()
        
        results = []
        for n in notifs:
            results.append({
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'is_read': n.is_read,
                'created_at': n.created_at.strftime("%d.%m.%Y %H:%M")
            })
            
        return JsonResponse({'success': True, 'unread_count': unread, 'notifications': results})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def mobile_admin_login(request):
    from django.contrib.auth import authenticate
    data = json.loads(request.body)
    user = authenticate(username=data.get('username'), password=data.get('password'))
    if user and user.is_staff:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def mobile_admin_messages(request):
    from django.contrib.auth import authenticate
    from django.core.paginator import Paginator
    from django.db.models import Q
    data = json.loads(request.body)
    if not authenticate(username=data.get('username'), password=data.get('password')):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    page = data.get('page', 1)
    search_q = data.get('search', '').strip()
    
    qs = ContactMessage.objects.all().order_by('-created_at')
    if search_q:
        qs = qs.filter(Q(full_name__icontains=search_q) | Q(subject__icontains=search_q) | Q(message__icontains=search_q))
        
    paginator = Paginator(qs, 20)
    try:
        page_obj = paginator.page(page)
        has_next = page_obj.has_next()
        results = page_obj.object_list
    except Exception:
        has_next = False
        results = []
        
    result = [{
        'id': m.id, 'full_name': m.full_name, 'subject': m.subject, 'message': m.message, 
        'is_replied': m.is_replied, 'created_at': m.created_at.strftime("%d.%m.%Y %H:%M"),
        'device_id': m.device_id
    } for m in results]
    
    return JsonResponse({'success': True, 'messages': result, 'has_next': has_next})

@csrf_exempt
def mobile_admin_reply(request):
    from django.contrib.auth import authenticate
    from .models import AppNotification
    data = json.loads(request.body)
    if not authenticate(username=data.get('username'), password=data.get('password')):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    msg = ContactMessage.objects.get(id=data.get('msg_id'))
    msg.is_replied = True
    msg.admin_notes = data.get('reply_text')
    msg.save()
    
    if msg.device_id:
        AppNotification.objects.create(
            device_id=msg.device_id,
            title="Talebinize Dönüş Yapıldı",
            message=data.get('reply_text')
        )
    return JsonResponse({'success': True})

@csrf_exempt
def mobile_admin_notify_all(request):
    from django.contrib.auth import authenticate
    from .models import AppNotification
    data = json.loads(request.body)
    if not authenticate(username=data.get('username'), password=data.get('password')):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    device_ids = set(AppNotification.objects.values_list('device_id', flat=True))
    device_ids.update(ContactMessage.objects.exclude(device_id__isnull=True).exclude(device_id='').values_list('device_id', flat=True))
    
    notifs = [AppNotification(device_id=d, title=data.get('title'), message=data.get('message')) for d in device_ids if d]
    AppNotification.objects.bulk_create(notifs)
    return JsonResponse({'success': True, 'count': len(notifs)})

@csrf_exempt
def mobile_admin_notify_selected(request):
    from django.contrib.auth import authenticate
    from .models import AppNotification, ContactMessage
    data = json.loads(request.body)
    if not authenticate(username=data.get('username'), password=data.get('password')):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    message_ids = data.get('message_ids', [])
    if not message_ids:
        return JsonResponse({'success': False, 'error': 'No messages selected'})
        
    msgs = ContactMessage.objects.filter(id__in=message_ids).exclude(device_id__isnull=True).exclude(device_id='')
    device_ids = set(msgs.values_list('device_id', flat=True))
    
    notifs = [AppNotification(device_id=d, title=data.get('title'), message=data.get('message')) for d in device_ids if d]
    AppNotification.objects.bulk_create(notifs)
    return JsonResponse({'success': True, 'count': len(notifs)})

@csrf_exempt
def mobile_admin_delete(request):
    from django.contrib.auth import authenticate
    from .models import ContactMessage
    data = json.loads(request.body)
    if not authenticate(username=data.get('username'), password=data.get('password')):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    message_ids = data.get('message_ids', [])
    ContactMessage.objects.filter(id__in=message_ids).delete()
    return JsonResponse({'success': True})
