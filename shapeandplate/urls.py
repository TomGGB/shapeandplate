from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workout/', include('workout.urls')),
    path('', include('home.urls')),
    path('', include('pwa.urls')),
    path('perfil/', include('perfil.urls')),
    path('plate/', include('plate.urls')),
    path('404/', TemplateView.as_view(template_name='404.html')),
]