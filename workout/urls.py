from django.urls import path
from django.urls import include
from workout import views

urlpatterns = [
    path('', views.workout, name='workout'),
]