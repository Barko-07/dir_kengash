import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import User, Region, PedagogicalCenter, Course

# Create Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin foydalanuvchisi yaratildi: Login: admin | Parol: admin123")
else:
    print("Admin foydalanuvchisi allaqachon mavjud.")

# Create Region and Center
region, created = Region.objects.get_or_create(name='Toshkent shahri')
center, created = PedagogicalCenter.objects.get_or_create(
    name='Toshkent Bosh Pedagogika Markazi',
    region=region,
    defaults={'address': 'Chilonzor tumani, Toshkent'}
)

if created:
    print("Boshlang'ich hudud va markaz qo'shildi.")

# Create Course
course, created = Course.objects.get_or_create(
    title='Maktabni boshqarishda zamonaviy usullar (AI)',
    defaults={
        'description': 'Ushbu kurs maktab direktorlariga ta\'lim jarayonini axborot texnologiyalari yordamida boshqarish sirlarini o\'rgatadi.',
        'is_active': True
    }
)

if created:
    print("Boshlang'ich o'quv kursi (Course) qo'shildi.")

print("Hammasi tayyor!")
