from django.urls import path, include
from . import views
from workout import views as workout_views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/save_data/', views.save_data, name='save_data'),
]