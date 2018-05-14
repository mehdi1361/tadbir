from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from employee.forms import UserCreationForm, PermissionForm
from .forms import LoginForm, UserRegistrationForm, \
    ProfileForm, FollowUpForm, PhoneFileForm, AddressForm, \
    DocumentForm, ReminderForm, RecoveryForm, SmsCautionForm, EmployeeFileForm, ChangePasswordForm, \
    UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import EmployeeFile, DocumentFile, PhoneFile, FollowUp, FileReminder, EmployeePermission
from bank.models import File, FileOffice
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from bank.models import PersonFile
from common.decorators import employee_permission
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

def user_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main'))
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
            return HttpResponseRedirect('/employee/login')

    else:
        user_form = UserRegistrationForm()

    return render(request, 'bank/employee/register.html', {'form': user_form})


@login_required(login_url='/employee/login/')
def dashboard(request):
    files_emp = EmployeeFile.objects.filter(employee=request.user).values_list('file', flat=True)
    follows = FollowUp.objects.filter(file__in=files_emp)[:8]
    reminders = FileReminder.objects.filter(file__in=files_emp).order_by('-created_at')[:10]
    last_files = EmployeeFile.files.filter(employee=request.user).order_by('-created_at')

    return render(
        request,
        'bank/employee/dashboard.html',
        {
            'follows': follows,
            'reminders': reminders,
            'files': last_files,
            'user': request.user
        }
    )


@login_required(login_url='/employee/login/')
@employee_permission('employee_file')
def files(request):
    query = request.POST.get('q')
    if query:
        person_File = PersonFile.objects.filter(person__name__contains=query).values_list('file__file_code', flat=True)
        office_files = FileOffice.objects.filter(office__name__contains=query).values_list('file__file_code', flat=True)
        employee_files = EmployeeFile.files.filter(employee=request.user).filter(
            Q(file__file_code__contains=query) | Q(file__contract_code__contains=query)
            | Q(file__file_code__in=person_File) | Q(file__file_code__in=office_files)
        )

    else:
        employee_files = EmployeeFile.files.filter(employee=request.user)
    return render(request, 'bank/employee/list.html', {'files': employee_files})


@login_required(login_url='/employee/login/')
def register_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES or None, instance=request.user.profile)

        if form.is_valid():
            form.save()

        else:
            print(form.errors)

    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'bank/employee/profile.html', {'form': form})


@login_required(login_url='/employee/login/')
@employee_permission('employee_file')
def file_document(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    recovery_sum = file.recoveries.filter(assurance_confirm=True).aggregate(sum=Sum('value'))
    follow_form = FollowUpForm(request.POST)
    phone_form = PhoneFileForm(request.POST)
    phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)

    address_form = AddressForm(request.POST)
    document_form = DocumentForm(request.POST, request.FILES or None)
    reminder_form = ReminderForm(request.POST)

    recovery_form = RecoveryForm(request.POST)
    sms_form = SmsCautionForm(request.POST)
    sms_form.fields['mobile_number'].queryset = PhoneFile.objects.filter(file=file)

    if request.method == 'POST':
        if follow_form.is_valid():
            result_follow_form = follow_form.save(commit=False)
            result_follow_form.file = file
            result_follow_form.save()
            messages.add_message(request, messages.SUCCESS, 'پیگیری با موفقیت ثبت شد.')

        # else:
        #     messages.add_message(request, messages.ERROR, 'خطا در ثبت پیگیری')

        if phone_form.is_valid():
            try:
                result_phone_form = phone_form.save(commit=False)
                result_phone_form.file = file
                result_phone_form.save()
                messages.add_message(request, messages.SUCCESS, 'شماره تماس با موفقیت ثبت شد')
                phone_form = PhoneFileForm()
                phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)

            except:
                messages.add_message(request, messages.ERROR, 'هشدار شماره تلفن تکراری است.')
                phone_form = PhoneFileForm()
                phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)

        else:
            print(phone_form.errors)
            phone_form = PhoneFileForm()
            phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)

        if address_form.is_valid():
            try:
                result_address_form = address_form.save(commit=False)
                result_address_form.file = file
                result_address_form.save()

                messages.add_message(request, messages.SUCCESS, 'آدرس با موفقیت ثبت شد.')

            except:
                messages.add_message(request, messages.ERROR, 'هشدار آدرس تکراری است.')

        if document_form.is_valid():
            try:

                result_document_form = document_form.save(commit=False)
                result_document_form.file = file
                result_document_form.save()

            except:
                pass

        if reminder_form.is_valid():
            try:

                result_reminder_form = reminder_form.save(commit=False)
                result_reminder_form.file = file
                result_reminder_form.save()

            except:
                pass

        if recovery_form.is_valid():
            try:
                result_recovery_form = recovery_form.save(commit=False)
                result_recovery_form.file = file
                result_recovery_form.save()

            except:
                pass

        if sms_form.is_valid():
            try:
                result_sms_form = sms_form.save(commit=False)
                result_sms_form.file = file
                result_sms_form.save()
                messages.add_message(request, messages.SUCCESS, 'پیامک با موفقیت ثبت شد')

            except:
                messages.add_message(request, messages.ERROR, 'هشدار پیامک تکراری است.')

    follow_form = FollowUpForm()
    phone_form = PhoneFileForm()
    phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)
    address_form = AddressForm()
    document_form = DocumentForm()
    reminder_form = ReminderForm()
    recovery_form = RecoveryForm()
    sms_form = SmsCautionForm()
    sms_form.fields['mobile_number'].queryset = PhoneFile.objects.filter(file=file)

    return render(
        request,
        'bank/employee/file_detail.html',
        {
            'file': file,
            'recovery_sum': recovery_sum['sum'] if recovery_sum['sum'] is not None else 0,
            'follow_form': follow_form,
            'phone_form': phone_form,
            'address_form': address_form,
            'document_form': document_form,
            'reminder_form': reminder_form,
            'recovery_form': recovery_form,
            'sms_form': sms_form
        }
    )


@login_required(login_url='/employee/login/')
@employee_permission('employee_file')
def edit_auth_employee_file(request, id):
    emp_file = EmployeeFile.objects.get(pk=id)
    if request.method == 'POST':
        form = EmployeeFileForm(request.POST, instance=emp_file)

        if form.is_valid():
            form.save()
            return redirect('bank:file_detail', file_id=emp_file.file.id)

    else:
        form = EmployeeFileForm(instance=emp_file)

    return render(request, 'bank/employee/employee_edit_auth.html', {'form': form})


@login_required(login_url='/employee/login/')
def change_password(request):
    form = ChangePasswordForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data

            if cd['new_password'] != cd['new_password']:
                messages.add_message(request, messages.ERROR, 'کلمه عبور جدید با تکرار کلمه عبور جدید یکسان نمی باشد.')
                form = ChangePasswordForm()

            else:
                request.user.set_password(cd['new_password'])
                request.user.save()
                messages.add_message(request, messages.SUCCESS, 'کلمه عبور با موفقیت تغییر یافت.')
                return HttpResponseRedirect(reverse('main'))
        else:
            messages.add_message(request, messages.ERROR, 'خطا در ثبت اطلاعات')
            form = ChangePasswordForm()

    else:
        form = ChangePasswordForm()

    return render(request, 'bank/employee/change_password.html', {'form': form})


def access_denied(request):
    return render(request, 'bank/employee/access_denied.html')


@login_required(login_url='/employee/login/')
@employee_permission('create_employee')
def create_employee(request):
    form = UserCreationForm(request.POST)
    users = User.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(username=cd['user_name'])
                messages.add_message(request, messages.ERROR, 'کاربر با این نام موجود است.')
                form = UserCreationForm()

            except:
                User.objects.create_user(username=cd['user_name'], password=1234, is_superuser=True)
                messages.add_message(request, messages.SUCCESS, 'کاربر با موفقیت ثبت شد.')
                form = UserCreationForm()
        else:
            messages.add_message(request, messages.ERROR, 'خطا در ثبت اطلاعات')
            form = ChangePasswordForm()

    else:
        form = UserCreationForm()

    return render(request, 'bank/employee/manage.html', {'form': form, 'users': users})


@login_required(login_url='/employee/login/')
@employee_permission('create_employee')
def employee_permission_view(request, emp_id):
    user = get_object_or_404(User, id=emp_id)
    employee_permission_lst = EmployeePermission.objects.filter(employee=user)
    return render(request, 'bank/employee/manage_employee.html',
                  {'user': user,
                   'permissions': employee_permission_lst
                   }
                  )


@login_required(login_url='/employee/login/')
@employee_permission('create_employee')
def edit_employee_permission(request, permission_id):
    permission = EmployeePermission.objects.get(pk=permission_id)
    if request.method == 'POST':
        form = PermissionForm(request.POST, instance=permission)

        if form.is_valid():
            form.save()
            return redirect('employee:permission', emp_id=permission.employee.id)

    else:
        form = PermissionForm(instance=permission)

    return render(request, 'bank/employee/manage_update.html', {'form': form, 'permission': permission})
