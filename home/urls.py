from django.urls import path
from home.views import index as index

urlpatterns = [
    path('', index, name='home'),
]