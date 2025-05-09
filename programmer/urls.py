from django.urls import path
from . import views

app_name = 'programmer'

urlpatterns = [
    path('home', views.home, name='programmer_home'),
    path('portfolio/create', views.create_portfolio, name='portfolio_create'),
    path('portfolio', views.view_portfolio, name='portfolio_view'),
    path('portfolio/edit', views.edit_portfolio, name='portfolio_edit'),
    path('orders', views.order_list, name='order_list'),
    path('place_a_bid/<int:order_id>', views.place_a_bid, name='place_a_bid'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('delete_subscription/<int:subscription_id>', views.delete_subscription, name='delete_subscription'),
    path('delete_bid/<int:bid_id>', views.delete_bid, name='delete_bid'),
]
