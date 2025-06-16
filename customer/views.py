from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from programmer.models import Portfolio
from .models import Order, Bid, Rating
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
def programmer_portfolio(request, user_id):
    portfolio = get_object_or_404(Portfolio, user=user_id)
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
    rating = None
    order = get_object_or_404(Order, id=order_id)
    if order.author == request.user:
        if not order.programmer:
            bids = order.bids.all().order_by('status')
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
        if order.is_rated:
            rating = Rating.objects.filter(order_id=order_id).first()
            rating = rating if rating else None
        return render(request, 'customer/order_detail.html',
                      {"order": order, "bids": bids, "comments": comments, "form": form, "rating": rating})
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


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
@require_POST
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, author=request.user)
    order.is_approved = True
    order.save()
    return redirect('customer:order_detail', order_id=order_id)


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
@require_POST
def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, author=request.user)
    order.is_rejected = True
    order.is_finished = False
    order.save()
    return redirect('customer:order_detail', order_id=order_id)


@user_passes_test(lambda u: u.groups.filter(name='Заказчик').exists())
@require_POST
def rate_order(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if order:
        if order.author == request.user:
            if order.is_approved:
                if not order.is_rated:
                    value = request.POST.get('rate')
                    try:
                        value = int(value)
                        if not (1 <= value <= 5):
                            return JsonResponse({'error': 'Оценка должна быть от 1 до 5.'}, status=400)
                    except (ValueError, TypeError):
                        return JsonResponse({'error': 'Некорректное значение оценки.'}, status=400)

                    created = Rating.objects.create(order=order,
                                                    user=request.user,
                                                    value=value)
                    if created:
                        order.is_rated = True
                        order.save()

                    return redirect('customer:order_detail', order_id=order_id)
