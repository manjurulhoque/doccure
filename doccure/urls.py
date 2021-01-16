from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('', include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
