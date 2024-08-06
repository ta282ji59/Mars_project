from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('map3d/', include('map3d.urls')),
    path('spectra/', include('spectra.urls')),
    path('api/',include('spectra.urls_api')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)