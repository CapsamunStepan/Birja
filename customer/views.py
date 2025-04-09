from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from programmer.models import Portfolio
from .models import Order, Bid, Comment
from .forms import OrderForm, CommentForm
from django.core.paginator import Paginator


# Create your views here.
@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def home(request):
    return render(request, 'customer/home.html')


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def programmers_list(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'customer/programmers.html', {"portfolios": portfolios})


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def programmer_portfolio(request, user):
    portfolio = get_object_or_404(Portfolio, user=user)
    return render(request, 'customer/programmer_portfolio.html', {"portfolio": portfolio})


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_list(request):
    orders = Order.objects.filter(author=request.user).order_by('-created')
    paginator = Paginator(orders, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'customer/order_list.html', {"orders": orders, "page_obj": page_obj})


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
    form = None
    order = get_object_or_404(Order, id=order_id)
    if order.author == request.user:
        if not order.programmer:
            bids = order.bids.all()
        else:
            bids = None
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    form.instance.order = order
                    form.instance.user = request.user
                    form.save()
                    form = CommentForm()
            else:
                form = CommentForm()
        comments = order.comments.all()
        return render(request, 'customer/order_detail.html',
                      {"order": order, "bids": bids, "comments": comments, "form": form})
    else:
        # access denied
        return redirect('customer:order_list')


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_edit(request, order_id):
    order = Order.objects.get(id=order_id)
    data = order.deadline
    if order.author == request.user:
        if request.method == 'POST':
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect(to='customer:order_detail', order_id=order_id)
        else:
            form = OrderForm(instance=order, initial={
                'deadline': order.deadline.strftime('%Y-%m-%d') if order.deadline else ''
            })

        return render(request, 'customer/order_edit.html', {'form': form, 'data': data})
    else:
        # access denied
        return redirect('customer:order_list')


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def order_delete(request, order_id):
    if request.method == 'POST':  # else access denied
        order = Order.objects.get(id=order_id)
        if order.author == request.user:  # else access denied
            if not order.programmer:  # else programmer should reject order
                order.delete()
    return redirect(to='customer:order_list')


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    if bid.order.author == request.user:
        if request.method == 'POST':
            bid.accept()
        return redirect('customer:order_detail', order_id=bid.order.id)
    else:
        # access denied
        return HttpResponse("Access denied")


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
def reject_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    if bid.order.author == request.user:
        if request.method == 'POST':
            bid.reject()
        return redirect('customer:order_detail', order_id=bid.order.id)
    else:
        # access denied
        return HttpResponse("Access denied")
