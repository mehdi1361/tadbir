from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.


def user_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('login success')
            else:
                return HttpResponse('disable user')

        else:
            return HttpResponse('invalid login')

    else:
        return render(request, 'bank/employee/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            return HttpResponse('ok')

    else:
            user_form = UserRegistrationForm()

    print(user_form.errors)
    return render(request, 'bank/employee/register.html', {'form': user_form})


@login_required(login_url='/employee/login/')
def dashboard(request):
    return render(request, 'bank/employee/dashboard.html')
