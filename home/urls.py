from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registration, name='register'),
    path('login/', views.authentication, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home:home'), name='logout'),

]
