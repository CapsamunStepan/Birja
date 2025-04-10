from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def home(request):
    if request.user.groups.filter(name='Программист').exists():
        return redirect(to='programmer:programmer_home')
    elif request.user.groups.filter(name='Заказчик').exists():
        return redirect(to='customer:customer_home')
    else:
        logout(request)
        return render(request, 'home/home.html')


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)  # User obj is created, but not is saved
            new_user.set_password(user_form.cleaned_data['password'])  # setting chosen password
            new_user.save()  # saving User
            group_id = user_form.cleaned_data['group'].id
            group = Group.objects.get(pk=group_id)
            group.user_set.add(new_user)
            login(request, new_user)
            return redirect(to='home:home')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'home/registration.html', {'user_form': user_form})


def authentication(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            next_url = request.POST.get('next', '')  # Получаем параметр next, если он есть
            if next_url:
                return HttpResponseRedirect(next_url)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.groups.filter(name='Программист').exists():
                        return redirect('programmer:programmer_home')
                    elif user.groups.filter(name='Заказчик').exists():
                        return redirect('customer:customer_home')
                    else:
                        pass

                else:
                    return HttpResponse("Disabled account")
        else:
            return HttpResponse("Invalid login")
    else:
        form = LoginForm
    return render(request, 'home/login.html', {'form': form})
