from django.urls import path
from . import views

app_name = 'programmer'

urlpatterns = [
    path('home', views.home, name='programmer_home'),
    path('portfolio/create', views.create_portfolio, name='portfolio_create'),
    path('portfolio', views.view_portfolio, name='portfolio_view'),
    path('portfolio/edit', views.edit_portfolio, name='portfolio_edit'),
]
