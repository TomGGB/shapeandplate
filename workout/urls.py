from django.urls import path
from workout import views

urlpatterns = [
    path('', views.workout, name='workout'),  # Ruta principal de workout
    path('generate_workout/', views.generate_workout, name='generate_workout'),
]