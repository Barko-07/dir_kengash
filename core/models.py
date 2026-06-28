from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        DIRECTOR = 'DIRECTOR', _('Director')
        TEACHER = 'TEACHER', _('Teacher')

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TEACHER)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PedagogicalCenter(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='centers')
    address = models.TextField(blank=True, null=True)
    director = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_center')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taught_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


# ─── New models for admin panel ───────────────────────────────────────────────

class BoardMember(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Ism va Familiya")
    position = models.CharField(max_length=255, verbose_name="Lavozim")
    bio = models.TextField(blank=True, verbose_name="Biografiya")
    photo = models.ImageField(upload_to='board_members/', null=True, blank=True, verbose_name="Rasm")
    photo_url = models.URLField(blank=True, null=True, verbose_name="Rasm URL (ixtiyoriy)")
    region = models.CharField(max_length=255, blank=True, verbose_name="Viloyat")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Ko'rinsin")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'full_name']
        verbose_name = "Kengash a'zosi"
        verbose_name_plural = "Kengash a'zolari"

    def get_photo(self):
        if self.photo:
            return self.photo.url
        return self.photo_url or 'https://ui-avatars.com/api/?name=' + self.full_name.replace(' ', '+') + '&background=0ea5e9&color=fff&size=200'

    def __str__(self):
        return f"{self.full_name} — {self.position}"


class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('talim', "Ta'lim"),
        ('yigilish', "Yig'ilish"),
        ('hamkorlik', "Hamkorlik"),
        ('boshqa', "Boshqa"),
    ]
    title = models.CharField(max_length=500, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")
    image = models.ImageField(upload_to='news/', null=True, blank=True, verbose_name="Rasm")
    image_url = models.URLField(blank=True, null=True, verbose_name="Rasm URL (ixtiyoriy)")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='boshqa', verbose_name="Kategoriya")
    published_at = models.DateField(auto_now_add=True, verbose_name="Sana")
    is_published = models.BooleanField(default=True, verbose_name="Nashr qilingan")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&q=80'

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    image = models.ImageField(upload_to='gallery/', null=True, blank=True, verbose_name="Rasm")
    image_url = models.URLField(blank=True, null=True, verbose_name="Rasm URL (ixtiyoriy)")
    caption = models.CharField(max_length=300, blank=True, verbose_name="Izoh")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Galereya rasmlari"

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

    def __str__(self):
        return self.caption or f"Rasm #{self.pk}"
