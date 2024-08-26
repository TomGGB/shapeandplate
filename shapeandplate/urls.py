from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workout/', include('workout.urls')),
    path('', RedirectView.as_view(url='workout/')),
    path('' , include('pwa.urls')),
    path('perfil/', include('perfil.urls')),
]