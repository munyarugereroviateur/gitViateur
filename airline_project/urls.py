
from django.contrib import admin

admin.site.site_header  = "Airline Ticketing System"
admin.site.site_title   = "Airline Admin"
admin.site.index_title  = "Welcome to Airline Administration"

from django.contrib import admin
from django.urls    import path, include
from django.conf    import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('flights.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)