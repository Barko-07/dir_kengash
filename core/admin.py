from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Region, PedagogicalCenter, Course, CourseEnrollment, BoardMember, NewsArticle, GalleryPhoto


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'avatar')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'region', 'is_active', 'order')
    list_filter = ('is_active', 'region')
    search_fields = ('full_name', 'position')
    list_editable = ('is_active', 'order')
    ordering = ('order',)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title',)
    list_editable = ('is_published',)


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'uploaded_at')
    search_fields = ('caption',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


admin.site.register(Region)
admin.site.register(PedagogicalCenter)
admin.site.register(CourseEnrollment)
