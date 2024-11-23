# plate/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.plate, name='plate'),
    path('delete_recipe/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
