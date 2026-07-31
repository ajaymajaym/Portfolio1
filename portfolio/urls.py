from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from core.admin_site import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
