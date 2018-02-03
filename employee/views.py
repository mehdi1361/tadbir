from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import EmployeeFile
# Create your views here.


def user_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(
                    reverse('main'))
                # return HttpResponse('login success')
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


@login_required(login_url='/employee/login/')
def files(request):
    employee_files = EmployeeFile.files.filter(employee=request.user)
    return render(request, 'bank/employee/list.html', {'files': employee_files})


@login_required(login_url='/employee/login/')
def register_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()

    else:
            form = ProfileForm(instance=request.user.profile)

    return render(request, 'bank/employee/profile.html', {'form': form})
