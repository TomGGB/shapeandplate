from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from workout.views import index  
from home.views import index as index
from django.views.generic import TemplateView

urlpatterns = [
    path('', index, name='home'),
]