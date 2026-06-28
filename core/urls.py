from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import admin_views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'centers', views.PedagogicalCenterViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # ── Public HTML views ────────────────────────────────────────
    path('', views.index_view, name='index'),
    path('setup/', views.setup_view, name='setup'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('board-members/', views.board_members_view, name='board_members'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('manager-course/', views.manager_course_view, name='manager_course'),
    path('profile/', views.profile_view, name='profile'),

    # ── Custom Admin Panel ───────────────────────────────────────
    path('admin-panel/login/', admin_views.admin_login_view, name='admin_login'),
    path('admin-panel/logout/', admin_views.admin_logout_view, name='admin_logout'),
    path('admin-panel/', admin_views.admin_dashboard_view, name='admin_dashboard'),

    # Board Members
    path('admin-panel/members/', admin_views.admin_members_view, name='admin_members'),
    path('admin-panel/members/add/', admin_views.admin_member_create_view, name='admin_member_create'),
    path('admin-panel/members/<int:pk>/edit/', admin_views.admin_member_edit_view, name='admin_member_edit'),
    path('admin-panel/members/<int:pk>/delete/', admin_views.admin_member_delete_view, name='admin_member_delete'),

    # News
    path('admin-panel/news/', admin_views.admin_news_view, name='admin_news'),
    path('admin-panel/news/add/', admin_views.admin_news_create_view, name='admin_news_create'),
    path('admin-panel/news/<int:pk>/edit/', admin_views.admin_news_edit_view, name='admin_news_edit'),
    path('admin-panel/news/<int:pk>/delete/', admin_views.admin_news_delete_view, name='admin_news_delete'),

    # Gallery
    path('admin-panel/gallery/', admin_views.admin_gallery_view, name='admin_gallery'),
    path('admin-panel/gallery/add/', admin_views.admin_gallery_create_view, name='admin_gallery_create'),
    path('admin-panel/gallery/<int:pk>/delete/', admin_views.admin_gallery_delete_view, name='admin_gallery_delete'),

    # Users
    path('admin-panel/users/', admin_views.admin_users_view, name='admin_users'),
    path('admin-panel/users/<int:pk>/edit/', admin_views.admin_user_edit_view, name='admin_user_edit'),
    path('admin-panel/users/<int:pk>/delete/', admin_views.admin_user_delete_view, name='admin_user_delete'),

    # Courses
    path('admin-panel/courses/', admin_views.admin_courses_view, name='admin_courses'),
    path('admin-panel/courses/add/', admin_views.admin_course_create_view, name='admin_course_create'),
    path('admin-panel/courses/<int:pk>/edit/', admin_views.admin_course_edit_view, name='admin_course_edit'),
    path('admin-panel/courses/<int:pk>/delete/', admin_views.admin_course_delete_view, name='admin_course_delete'),
]
