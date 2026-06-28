from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User, Region, PedagogicalCenter, Course, CourseEnrollment, BoardMember, NewsArticle, GalleryPhoto
from .serializers import (
    UserSerializer, RegionSerializer, PedagogicalCenterSerializer, 
    CourseSerializer, CourseEnrollmentSerializer
)

# ============================
# HTML Template Views
# ============================

def index_view(request):
    news = NewsArticle.objects.filter(is_published=True)[:3]
    members = BoardMember.objects.filter(is_active=True)[:3]
    return render(request, 'index.html', {'news': news, 'members': members})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Noto\'g\'ri login yoki parol'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', 'direktor')

        if not username:
            return render(request, 'register.html', {'error': 'Foydalanuvchi nomi kiritilishi shart'})
        if not password:
            return render(request, 'register.html', {'error': 'Parol kiritilishi shart'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Bu foydalanuvchi nomi band'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = role
        user.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})

def board_members_view(request):
    members = BoardMember.objects.filter(is_active=True)
    return render(request, 'board_members.html', {'members': members})

def gallery_view(request):
    photos = GalleryPhoto.objects.all()
    return render(request, 'gallery.html', {'photos': photos})

def manager_course_view(request):
    return render(request, 'managerial_course.html')



@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        phone = request.POST.get('phone_number', '').strip()
        if phone:
            user.phone_number = phone
        user.save()
        return render(request, 'profile.html', {'success': "Profil muvaffaqiyatli yangilandi!"})
    return render(request, 'profile.html')


# ============================
# REST API ViewSets
# ============================

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer

class PedagogicalCenterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PedagogicalCenter.objects.all()
    serializer_class = PedagogicalCenterSerializer


