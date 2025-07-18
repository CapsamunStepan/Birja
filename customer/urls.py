from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('home', views.home, name='customer_home'),
    path('programmers', views.programmers_list, name='programmers_list'),
    path('programmer/<int:user_id>', views.programmer_portfolio, name='programmer_portfolio'),
    path('create_order', views.order_create, name='order_create'),
    path('orders', views.order_list, name='order_list'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('edit_order/<int:order_id>', views.order_edit, name='order_edit'),
    path('delete_order/<int:order_id>', views.order_delete, name='order_delete'),
    path('accept_bid/<int:bid_id>', views.accept_bid, name='accept_bid'),
    path('reject_bid/<int:bid_id>', views.reject_bid, name='reject_bid'),
    path('approve_order/<int:order_id>', views.approve_order, name='approve_order'),
    path('reject_order/<int:order_id>', views.reject_order, name='reject_order'),
    path('rate/<int:order_id>', views.rate_order, name='rate_order'),
]
