from django.urls import path
from django.urls import include
from workout import views

urlpatterns = [
    path('workout/', views.workout, name='workout'),
    path('workout/generate_workout/', views.generate_workout, name='generate_workout'),
]