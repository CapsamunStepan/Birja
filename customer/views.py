from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from programmer.models import Portfolio
from .models import Order, Bid, Comment
from .forms import OrderForm


# Create your views here.
@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def home(request):
    return render(request, 'customer/home.html')


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def programmers_list(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'customer/programmers.html', {"portfolios": portfolios})


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def orders_list(request):
    orders = Order.objects.filter(author=request.user).order_by('-created')
    return render(request, 'customer/orders_list.html', {"orders": orders})


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user  # Присваиваем пользователя
            order.save()
            return redirect(to='customer:orders_list')
    else:
        form = OrderForm()
    return render(request, 'customer/order_create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.author == request.user:
        if not order.programmer:
            bids = order.bids.all()
            comments = None
        else:
            comments = order.comments.all()
            bids = None
        return render(request, 'customer/order_detail.html',
                      {"order": order, "bids": bids, "comments": comments})
    else:
        # access denied
        return redirect('customer:orders_list')


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_edit(request, order_id):
    pass
