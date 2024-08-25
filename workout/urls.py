from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import include
from workout import views

urlpatterns = [
    #redireccionar a workout
    path('', RedirectView.as_view(url='workout/', permanent=True)),
    path('workout/', views.workout, name='workout'),
    path('workout/generate_workout/', views.generate_workout, name='generate_workout'),
]