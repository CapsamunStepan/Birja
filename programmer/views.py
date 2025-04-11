from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from customer.forms import CommentForm
from .models import Portfolio
from .forms import PortfolioForm, BidForm
from customer.models import Order, Bid


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def home(request):
    link = ''
    portfolio = Portfolio.objects.filter(user_id=request.user.id).first()
    has_portfolio = portfolio is not None
    if portfolio:
        token = portfolio.telegram_link_token
        if not token:
            token = portfolio.generate_telegram_token()
        link = f"https://t.me/it_birja_bot?start={token}"
    return render(
        request,
        'programmer/home.html',
        {'has_portfolio': has_portfolio, "link": link},
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
    form = BidForm()
    user_bids = Bid.objects.filter(programmer=request.user).values_list('order_id', flat=True)
    return render(request, 'programmer/order_list.html',
                  {'orders': orders, 'form': form, 'user_bids': user_bids})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def place_a_bid(request, order_id):
    order = get_object_or_404(Order, id=order_id, programmer=None)
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


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    bid = request.user.bids.filter(order=order).first()
    if order:
        if order.programmer is None:
            return render(request, 'programmer/order_detail.html', {'order': order, 'bid': bid})
        elif order.programmer.id == bid.programmer.id:
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
            return render(request, 'programmer/order_detail.html',
                          {'order': order, 'bid': bid, 'form': form, 'comments': comments})
        # else access denied
        return redirect('programmer:order_list')


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def my_orders(request):
    orders = Order.objects.filter(programmer=request.user).order_by('-taken')
    bids = Bid.objects.filter(programmer=request.user).order_by('status')
    return render(request, 'programmer/my_orders.html', {'orders': orders, 'bids': bids})


# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def news_view(request):
#     news = News.objects.filter().order_by('-published')
#     return render(request, 'programmer/news_view.html', {'news': news})
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
