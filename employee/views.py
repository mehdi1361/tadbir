from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm, \
    ProfileForm, FollowUpForm, PhoneFileForm, AddressForm, DocumentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import EmployeeFile,DocumentFile
from bank.models import File
from django.shortcuts import get_object_or_404
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


@login_required(login_url='/employee/login/')
def file_document(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    follow_form = FollowUpForm(request.POST)
    phone_form = PhoneFileForm(request.POST)
    address_form = AddressForm(request.POST)
    document_form = DocumentForm(request.POST, request.FILES)

    if request.method == 'POST':
        if follow_form.is_valid():
            result_follow_form = follow_form.save(commit=False)
            result_follow_form.file = file
            result_follow_form.save()

        else:
            follow_form = FollowUpForm()

        if phone_form.is_valid():
            try:
                result_phone_form = phone_form.save(commit=False)
                result_phone_form.file = file
                result_phone_form.save()

            except:
                pass

        else:
            phone_form = PhoneFileForm()

        if address_form.is_valid():
            try:
                result_address_form = address_form.save(commit=False)
                result_address_form.file = file
                result_address_form.save()

            except:
                pass

        else:
            address_form = AddressForm()

        if document_form.is_valid():
            # try:
            new_doc = DocumentFile(
                image_upload=request.FILES['image_upload'],
                type=request.POST['type'],
                description=request.POST['description']
            )
            new_doc.save()
                # result_document_form = document_form.save(commit=False)
                # result_document_form.file = file
                # result_document_form.save()

            # except:
            #     pass

        document_form = DocumentForm()

    else:
        follow_form = FollowUpForm()
        phone_form = PhoneFileForm()
        address_form = AddressForm()
        document_form = DocumentForm()

    return render(
        request,
        'bank/employee/file_detail.html',
        {
            'file': file,
            'follow_form': follow_form,
            'phone_form': phone_form,
            'address_form': address_form,
            'document_form': document_form
        }
    )


