from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from workout.views import index  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workout/', include('workout.urls')),
    path('', index, name='index'),
    path('', include('pwa.urls')),
    path('perfil/', include('perfil.urls')),
    path('plate/', include('plate.urls')),
]