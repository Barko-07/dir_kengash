from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from functools import wraps

from .models import BoardMember, NewsArticle, GalleryPhoto, User, Course, CourseEnrollment
from .admin_forms import BoardMemberForm, NewsArticleForm, GalleryPhotoForm, UserEditForm, CourseForm


# ─── Security Decorator ──────────────────────────────────────────────────────
def admin_required(view_func):
    """Allow only is_staff=True users."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if not request.user.is_staff:
            return render(request, 'admin_403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Admin Auth ───────────────────────────────────────────────────────────────
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': "Noto'g'ri login/parol yoki sizda admin huquqi yo'q."})
    return render(request, 'admin_login.html')


def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')


# ─── Dashboard ────────────────────────────────────────────────────────────────
@admin_required
def admin_dashboard_view(request):
    ctx = {
        'total_users': User.objects.count(),
        'total_members': BoardMember.objects.count(),
        'active_members': BoardMember.objects.filter(is_active=True).count(),
        'total_news': NewsArticle.objects.count(),
        'published_news': NewsArticle.objects.filter(is_published=True).count(),
        'total_gallery': GalleryPhoto.objects.count(),
        'total_courses': Course.objects.count(),
        'active_courses': Course.objects.filter(is_active=True).count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_news': NewsArticle.objects.order_by('-published_at')[:5],
    }
    return render(request, 'admin_dashboard.html', ctx)


# ─── Board Members ────────────────────────────────────────────────────────────
@admin_required
def admin_members_view(request):
    q = request.GET.get('q', '')
    members = BoardMember.objects.all()
    if q:
        members = members.filter(Q(full_name__icontains=q) | Q(position__icontains=q))
    return render(request, 'admin_members.html', {'members': members, 'q': q})


@admin_required
def admin_member_create_view(request):
    form = BoardMemberForm()
    if request.method == 'POST':
        form = BoardMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "A'zo muvaffaqiyatli qo'shildi!")
            return redirect('admin_members')
    return render(request, 'admin_member_form.html', {'form': form, 'action': 'Qo\'shish'})


@admin_required
def admin_member_edit_view(request, pk):
    member = get_object_or_404(BoardMember, pk=pk)
    form = BoardMemberForm(instance=member)
    if request.method == 'POST':
        form = BoardMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "A'zo ma'lumotlari yangilandi!")
            return redirect('admin_members')
    return render(request, 'admin_member_form.html', {'form': form, 'action': 'Tahrirlash', 'member': member})


@admin_required
def admin_member_delete_view(request, pk):
    member = get_object_or_404(BoardMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "A'zo o'chirildi.")
        return redirect('admin_members')
    return render(request, 'admin_confirm_delete.html', {'object': member, 'type': "Kengash a'zosi"})


# ─── News ─────────────────────────────────────────────────────────────────────
@admin_required
def admin_news_view(request):
    q = request.GET.get('q', '')
    news = NewsArticle.objects.all()
    if q:
        news = news.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'admin_news.html', {'news': news, 'q': q})


@admin_required
def admin_news_create_view(request):
    form = NewsArticleForm()
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangilik qo'shildi!")
            return redirect('admin_news')
    return render(request, 'admin_news_form.html', {'form': form, 'action': 'Qo\'shish'})


@admin_required
def admin_news_edit_view(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    form = NewsArticleForm(instance=article)
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangilik yangilandi!")
            return redirect('admin_news')
    return render(request, 'admin_news_form.html', {'form': form, 'action': 'Tahrirlash', 'article': article})


@admin_required
def admin_news_delete_view(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, "Yangilik o'chirildi.")
        return redirect('admin_news')
    return render(request, 'admin_confirm_delete.html', {'object': article, 'type': 'Yangilik'})


# ─── Gallery ──────────────────────────────────────────────────────────────────
@admin_required
def admin_gallery_view(request):
    photos = GalleryPhoto.objects.all()
    return render(request, 'admin_gallery.html', {'photos': photos})


@admin_required
def admin_gallery_create_view(request):
    form = GalleryPhotoForm()
    if request.method == 'POST':
        form = GalleryPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Rasm qo'shildi!")
            return redirect('admin_gallery')
    return render(request, 'admin_gallery_form.html', {'form': form, 'action': 'Qo\'shish'})


@admin_required
def admin_gallery_delete_view(request, pk):
    photo = get_object_or_404(GalleryPhoto, pk=pk)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, "Rasm o'chirildi.")
        return redirect('admin_gallery')
    return render(request, 'admin_confirm_delete.html', {'object': photo, 'type': 'Galereya rasmi'})


# ─── Users ────────────────────────────────────────────────────────────────────
@admin_required
def admin_users_view(request):
    q = request.GET.get('q', '')
    users = User.objects.all().order_by('-date_joined')
    if q:
        users = users.filter(Q(username__icontains=q) | Q(email__icontains=q))
    return render(request, 'admin_users.html', {'users': users, 'q': q})


@admin_required
def admin_user_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserEditForm(instance=user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Foydalanuvchi ma'lumotlari yangilandi!")
            return redirect('admin_users')
    return render(request, 'admin_user_form.html', {'form': form, 'edited_user': user})


@admin_required
def admin_user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "O'zingizni o'chirib bo'lmaydi!")
        return redirect('admin_users')
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Foydalanuvchi o'chirildi.")
        return redirect('admin_users')
    return render(request, 'admin_confirm_delete.html', {'object': user, 'type': 'Foydalanuvchi'})


# ─── Courses ──────────────────────────────────────────────────────────────────
@admin_required
def admin_courses_view(request):
    courses = Course.objects.all()
    return render(request, 'admin_courses.html', {'courses': courses})


@admin_required
def admin_course_create_view(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kurs qo'shildi!")
            return redirect('admin_courses')
    return render(request, 'admin_course_form.html', {'form': form, 'action': 'Qo\'shish'})


@admin_required
def admin_course_edit_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Kurs yangilandi!")
            return redirect('admin_courses')
    return render(request, 'admin_course_form.html', {'form': form, 'action': 'Tahrirlash', 'course': course})


@admin_required
def admin_course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Kurs o'chirildi.")
        return redirect('admin_courses')
    return render(request, 'admin_confirm_delete.html', {'object': course, 'type': 'Kurs'})
