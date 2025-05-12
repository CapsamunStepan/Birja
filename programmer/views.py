from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from customer.forms import CommentForm
from .models import Portfolio, CategorySubscription
from .forms import PortfolioForm, CategorySubscriptionForm, BidForm
from customer.models import Order, Bid
from django.core.paginator import Paginator


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def home(request):
    link = ''
    subscriptions = None
    form = CategorySubscriptionForm(request.POST or None)
    portfolio = Portfolio.objects.filter(user_id=request.user.id).first()
    has_portfolio = portfolio is not None
    if portfolio:
        token = portfolio.telegram_link_token
        if not token:
            token = portfolio.generate_telegram_token()
        link = f"https://t.me/it_birja_bot?start={token}"
        subscriptions = CategorySubscription.objects.filter(user=request.user)
        if request.method == 'POST':
            if form.is_valid():
                cd = form.cleaned_data
                if cd['category'] not in [x.category for x in subscriptions]:
                    new_subscription = form.save(commit=False)
                    new_subscription.user = request.user
                    new_subscription.save()
                    return redirect(to='programmer:programmer_home')
                else:
                    form.add_error('category', 'Вы уже подписаны на эту категорию.')
    return render(
        request,
        'programmer/home.html',
        {'has_portfolio': has_portfolio, "link": link, "subscriptions": subscriptions, 'form': form},
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
    sort = request.GET.get('sort', 'deadline')
    filter_type = request.GET.get('filter', 'all')

    allowed_sorts = {
        'deadline': 'deadline',
        'deadline_desc': '-deadline',
        'price': 'price',
        'price_desc': '-price',
    }
    sort_field = allowed_sorts.get(sort, 'deadline')
    orders = Order.objects.filter(programmer=None)
    user_bids = Bid.objects.filter(programmer=request.user).values_list('order_id', flat=True)

    if filter_type == 'new':
        orders = orders.exclude(id__in=user_bids)
    elif filter_type == 'submitted':
        orders = orders.filter(id__in=user_bids)

    orders = orders.order_by(sort_field)
    paginator = Paginator(orders, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = BidForm()

    return render(request, 'programmer/order_list.html', {
        'orders': orders,
        'form': form,
        'user_bids': user_bids,
        'current_sort': sort,
        'current_filter': filter_type,
        'page_obj': page_obj,
    })


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def place_a_bid(request, order_id):
    order = get_object_or_404(Order, id=order_id, programmer=None)
    if not order:
        return redirect('programmer:order_list')

    if Bid.objects.filter(order=order, programmer=request.user).exists():
        return redirect('programmer:order_detail', order_id=order_id)

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.programmer = request.user
            bid.order = order
            bid.save()
            return redirect('programmer:order_detail', order_id=order_id)


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    bid = request.user.bids.filter(order=order).first()
    if order:
        if order.programmer is None:
            return render(request, 'programmer/order_detail.html', {'order': order, 'bid': bid})
        elif order.programmer == request.user:
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
    sort = request.GET.get('sort', 'deadline')
    allowed_sorts = {
        'deadline': 'deadline',
        'deadline_desc': '-deadline',
        'price': 'price',
        'price_desc': '-price',
    }
    sort_field = allowed_sorts.get(sort, 'deadline')
    orders = Order.objects.filter(programmer=request.user).order_by(sort_field)
    bids = Bid.objects.filter(programmer=request.user).order_by('status')
    return render(request, 'programmer/my_orders.html', {
        'orders': orders,
        'bids': bids,
        'current_sort': sort,
    })


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def delete_subscription(request, subscription_id):
    subscription = CategorySubscription.objects.filter(id=subscription_id).first()
    if subscription:
        if subscription.user == request.user:
            if request.method == "POST":
                subscription.delete()
            return redirect(to='programmer:programmer_home')
        else:
            # access denied
            pass


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
@require_POST
def delete_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, programmer=request.user)
    bid.delete()
    return redirect(to='programmer:my_orders')


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
@require_POST
def finish_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, programmer=request.user)
    order.is_finished = True
    order.is_rejected = False
    order.save()
    return redirect(to='programmer:order_detail', order_id=order_id)

# @user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
# def news_view(request):
#     news = News.objects.filter().order_by('-published')
#     return render(request, 'programmer/news_view.html', {'news': news})
