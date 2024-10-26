from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('', redirect_to_home, name='root'),  # Nueva línea para redirigir
    path('admin/', admin.site.urls),
    path('workout/', include('workout.urls')),
    path('perfil/', include('perfil.urls')),
    path('plate/', include('plate.urls')),
    path('home/', include('home.urls')),
]
