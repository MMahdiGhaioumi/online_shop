from django.urls import path, include
from django.conf.urls.static import static
from account.admin import my_admin_site
from . import settings

urlpatterns = [
    path('admin/', my_admin_site.urls),
    path('', include('home.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
