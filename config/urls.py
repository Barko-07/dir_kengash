from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# pyrefly: ignore [missing-import]
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin.site.site_header = 'Direktorlar Kengashi Boshqaruvi'
admin.site.site_title = 'Boshqaruv Paneli'
admin.site.index_title = 'Boshqaruv Paneliga Xush Kelibsiz'

urlpatterns = [
    # Asl Django admin panelini yashirin (xavfsiz) manzilga o'tkazdik
    path('maxfiy-admin/', admin.site.urls),
    
    # SimpleJWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Core app URLs
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
