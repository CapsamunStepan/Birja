from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import Portfolio
from .forms import PortfolioForm


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
    has_portfolio = portfolio is not None

    if has_portfolio:
        return redirect('programmer:programmer_home')

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_id = request.user.id
            form.save()
            return render(request, 'programmer/portfolio_view.html', {'portfolio': portfolio})
    else:
        form = PortfolioForm()

    return render(request, 'programmer/portfolio_create.html', {'form': form, 'has_portfolio': has_portfolio})


@user_passes_test(lambda u: u.groups.filter(name='Программист').exists())
def view_portfolio(request):
    portfolio = Portfolio.objects.filter(user_id=request.user.id).first()
    if not portfolio:
        return redirect('programmer:portfolio_create')
    url = portfolio.image.url
    image_url = ''
    for x in range(19, len(url)):
        image_url += url[x]

    return render(request, 'programmer/portfolio_view.html', {'portfolio': portfolio, 'image_url': image_url})


def edit_portfolio(request):
    return None