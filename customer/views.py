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
def order_list(request):
    orders = Order.objects.filter(author=request.user).order_by('-created')
    return render(request, 'customer/order_list.html', {"orders": orders})


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user  # Присваиваем пользователя
            order.save()
            return redirect(to='customer:order_list')
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
        return redirect('customer:order_list')


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_edit(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.author == request.user:
        if request.method == 'POST':
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect(to='customer:order_detail', order_id=order_id)
        else:
            form = OrderForm(instance=order)
        return render(request, 'customer/order_edit.html', {'form': form})
    else:
        # access denied
        return redirect('customer:order_list')


def order_delete(request, order_id):
    if request.method == 'POST':  # else access denied
        order = Order.objects.get(id=order_id)
        if order.author == request.user:  # else access denied
            if not order.programmer:  # else programmer should reject order
                order.delete()
    return redirect(to='customer:order_list')

