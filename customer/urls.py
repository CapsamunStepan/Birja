from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('home', views.home, name='customer_home'),
    path('programmers', views.programmers_list, name='programmers_list'),
    path('create_order', views.order_create, name='order_create'),
    path('orders', views.orders_list, name='orders_list'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
]
