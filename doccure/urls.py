import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Doccure Admin"
admin.site.site_title = "Doccure Admin Portal"
admin.site.index_title = "Welcome to Doccure Doctore and Patient Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('patients/', include("patients.urls")),
    path('', include("core.urls")),

    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
