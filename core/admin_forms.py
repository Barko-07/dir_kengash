from django import forms
from .models import BoardMember, NewsArticle, GalleryPhoto, User, Course


class BoardMemberForm(forms.ModelForm):
    class Meta:
        model = BoardMember
        fields = ['full_name', 'position', 'bio', 'photo', 'photo_url', 'region', 'phone', 'email', 'order', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'admin-input', 'placeholder': "Ism va Familiya"}),
            'position': forms.TextInput(attrs={'class': 'admin-input', 'placeholder': "Lavozim"}),
            'bio': forms.Textarea(attrs={'class': 'admin-input', 'rows': 4, 'placeholder': "Qisqacha tarjimai hol..."}),
            'photo_url': forms.URLInput(attrs={'class': 'admin-input', 'placeholder': "https://..."}),
            'region': forms.TextInput(attrs={'class': 'admin-input', 'placeholder': "Toshkent"}),
            'phone': forms.TextInput(attrs={'class': 'admin-input', 'placeholder': "+998 90 123 45 67"}),
            'email': forms.EmailInput(attrs={'class': 'admin-input', 'placeholder': "email@example.com"}),
            'order': forms.NumberInput(attrs={'class': 'admin-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'admin-checkbox'}),
        }


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content', 'image', 'image_url', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'admin-input', 'placeholder': "Yangilik sarlavhasi"}),
            'content': forms.Textarea(attrs={'class': 'admin-input', 'rows': 6, 'placeholder': "Yangilik matni..."}),
            'image_url': forms.URLInput(attrs={'class': 'admin-input', 'placeholder': "https://images.unsplash.com/..."}),
            'category': forms.Select(attrs={'class': 'admin-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'admin-checkbox'}),
        }


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ['image', 'image_url', 'caption']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'admin-input', 'placeholder': "https://..."}),
            'caption': forms.TextInput(attrs={'class': 'admin-input', 'placeholder': "Rasm haqida qisqacha izoh"}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'admin-input'}),
            'first_name': forms.TextInput(attrs={'class': 'admin-input'}),
            'last_name': forms.TextInput(attrs={'class': 'admin-input'}),
            'email': forms.EmailInput(attrs={'class': 'admin-input'}),
            'role': forms.Select(attrs={'class': 'admin-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'admin-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'admin-checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'admin-checkbox'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'admin-input', 'placeholder': "Kurs nomi"}),
            'description': forms.Textarea(attrs={'class': 'admin-input', 'rows': 5, 'placeholder': "Kurs haqida ma'lumot..."}),
            'instructor': forms.Select(attrs={'class': 'admin-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'admin-checkbox'}),
        }
