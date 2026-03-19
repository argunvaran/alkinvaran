from django.db import models

class Lesson(models.Model):
    DAYS_OF_WEEK = [
        ('1', 'Pazartesi'),
        ('2', 'Salı'),
        ('3', 'Çarşamba'),
        ('4', 'Perşembe'),
        ('5', 'Cuma'),
        ('6', 'Cumartesi'),
        ('7', 'Pazar'),
    ]
    name = models.CharField(max_length=200, verbose_name="Ders Adı (Örn: Çocuk Cimnastik)")
    day_of_week = models.CharField(max_length=1, choices=DAYS_OF_WEEK, verbose_name="Gün")
    time = models.TimeField(verbose_name="Saat")
    notes = models.TextField(blank=True, null=True, verbose_name="Açıklama/Notlar")

    @property
    def friendly_name(self):
        day = self.get_day_of_week_display()
        time_str = self.time.strftime('%I:%M %p').lstrip('0')
        return f"{self.name} {day} {time_str}"

    def __str__(self):
        return self.friendly_name

    class Meta:
        verbose_name = "Ders"
        verbose_name_plural = "Dersler"
        ordering = ['day_of_week', 'time']

class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('inactive', 'Pasif'),
    ]
    
    full_name = models.CharField(max_length=200, verbose_name="Öğrenci Adı Soyadı")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="E-posta")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Durum")
    lessons = models.ManyToManyField(Lesson, related_name='students', blank=True, verbose_name="Kayıtlı Olduğu Dersler")
    notes = models.TextField(blank=True, null=True, verbose_name="Özel Notlar")
    
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Öğrenci"
        verbose_name_plural = "Öğrenciler"
        ordering = ['-registration_date']

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Nakit'),
        ('transfer', 'EFT/Havale'),
        ('cc', 'Kredi Kartı'),
    ]
    MONTH_CHOICES = [
        (1, 'Ocak'), (2, 'Şubat'), (3, 'Mart'), (4, 'Nisan'),
        (5, 'Mayıs'), (6, 'Haziran'), (7, 'Temmuz'), (8, 'Ağustos'),
        (9, 'Eylül'), (10, 'Ekim'), (11, 'Kasım'), (12, 'Aralık')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments', verbose_name="Öğrenci")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', verbose_name="İlgili Ders")
    payment_month = models.IntegerField(choices=MONTH_CHOICES, verbose_name="Ödeme Ayı", blank=True, null=True)
    payment_year = models.IntegerField(verbose_name="Ödeme Yılı", blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar (₺)")
    payment_date = models.DateField(verbose_name="Ödeme Tarihi")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='transfer', verbose_name="Ödeme Yöntemi")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Açıklama (Örn: Mart Ayı Aidatı)")
    
    def __str__(self):
        return f"{self.student.full_name} - {self.amount}₺"

    class Meta:
        verbose_name = "Ödeme"
        verbose_name_plural = "Ödemeler"
        ordering = ['-payment_date']


class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('rent', 'Kira / Alan Aidatı'),
        ('salary', 'Maaş / Personel'),
        ('bills', 'Fatura (Elektrik/Su/İnternet)'),
        ('equipment', 'Ekipman / Malzeme'),
        ('marketing', 'Reklam / Pazarlama'),
        ('cleaning', 'Temizlik / Hijyen'),
        ('other', 'Diğer'),
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar (₺)")
    date = models.DateField(verbose_name="Gider Tarihi")
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES, default='other', verbose_name="Kategori")
    description = models.CharField(max_length=255, verbose_name="Açıklama / Detay")
    
    expense_month = models.IntegerField(choices=Payment.MONTH_CHOICES, verbose_name="İlgili Ay", blank=True, null=True)
    expense_year = models.IntegerField(verbose_name="İlgili Yıl", blank=True, null=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.amount}₺"

    class Meta:
        verbose_name = "Gider"
        verbose_name_plural = "Giderler"
        ordering = ['-date']
