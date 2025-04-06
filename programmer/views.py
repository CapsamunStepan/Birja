from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import Portfolio
from .forms import PortfolioForm, BidForm
from customer.models import Order, Bid


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def home(request):
    portfolio = Portfolio.objects.filter(user_id=request.user.id).first()
    has_portfolio = portfolio is not None
    return render(
        request,
        'programmer/home.html',
        {'has_portfolio': has_portfolio}
    )


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def create_portfolio(request):
    portfolio = Portfolio.objects.filter(user_id=request.user.id).first()

    if portfolio:
        return redirect('programmer:programmer_home')

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_id = request.user.id
            form.save()
            return redirect(to='programmer:portfolio_view')
    else:
        form = PortfolioForm()

    return render(request, 'programmer/portfolio_create.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def view_portfolio(request):
    portfolio = Portfolio.objects.filter(user_id=request.user.id).first()
    if not portfolio:
        return redirect('programmer:portfolio_create')
    return render(request, 'programmer/portfolio_view.html', {'portfolio': portfolio})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def edit_portfolio(request):
    portfolio = Portfolio.objects.filter(user_id=request.user.id).first()
    if not portfolio:
        return redirect('programmer:portfolio_create')
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect(to='programmer:portfolio_view')
    else:
        form = PortfolioForm(instance=portfolio)

    return render(request, 'programmer/portfolio_edit.html', {'form': form, 'portfolio': portfolio})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def order_list(request):
    orders = Order.objects.filter(programmer=None).order_by('-created')
    return render(request, 'programmer/order_list.html', {'orders': orders})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def place_a_bid(request, order_id):
    order = Order.objects.filter(id=order_id, programmer=None).first()
    if not order:
        return redirect('programmer:order_list')

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.programmer = request.user
            bid.order = order
            bid.save()
            return redirect('programmer:order_list')
    else:
        form = BidForm()

    return render(request, 'programmer/order_list.html', {'form': form, 'order': order})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def order_detail(request, order_id):
    order = Order.objects.filter(id=order_id, programmer=None)
    if not order:
        return redirect('programmer:order_list')
    else:
        return render(request, 'programmer/order_detail.html', {'order': order})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def my_orders(request):
    orders = Order.objects.filter(programmer=request.user).order_by('-taken')
    return render(request, 'programmer/my_orders.html', {'orders': orders})




# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def take_order(request):
#     order_id = request.POST.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#
#     # Проверка, чтобы нельзя было взять заказ, если он уже взят другим программистом
#     if order.programmer_id is not None:
#         return HttpResponseForbidden("Этот заказ уже взят")
#
#     # Установка programmer_id на ваш идентификатор пользователя
#     order.programmer_id = request.user.id
#     order.taken = timezone.now()
#     order.save()
#     orders = Order.objects.filter(programmer_id=request.user.id)
#     return render(request, 'programmer/taken-orders.html', {'orders': orders})
#
#
# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def delete_order(request):
#     order_id = request.POST.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#
#     # Проверка если заказ взят программистом
#     if order.programmer_id:
#         order.programmer_id = None
#         order.taken = None
#         order.save()
#
#     orders = Order.objects.filter(programmer_id=request.user.id)
#     return render(request, 'programmer/taken-orders.html', {'orders': orders})
#
#
# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def news_view(request):
#     news = News.objects.filter().order_by('-published')
#     return render(request, 'programmer/news_view.html', {'news': news})
#
#
# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def taken_orders(request):
#     orders = Order.objects.filter(programmer_id=request.user.id)
#     return render(request, 'programmer/taken-orders.html', {'orders': orders})
#
#
# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def contacts(request):
#     return render(request, 'programmer/contacts.html')
#
#
# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def view_order_detail(request, order_id):
#     # order_id = request.POST.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if 'done_button' in request.POST:
#             order.is_done = True
#             order.save()
#         elif 'edit_button' in request.POST:
#             order.is_done = False
#             order.save()
#         elif 'add_comm' in request.POST:
#             if form.is_valid():
#                 form.instance.order = order
#                 form.instance.user = request.user
#                 form.save()
#                 form = CommentForm()
#     else:
#         form = CommentForm()
#     comments = order.comments.all()
#     return render(request, 'programmer/view_order_detail.html', {"order": order,
#                                                                  "comments": comments,
#                                                                  "form": form})
