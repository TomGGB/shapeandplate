from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]