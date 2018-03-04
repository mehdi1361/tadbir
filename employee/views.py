from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm, \
    ProfileForm, FollowUpForm, PhoneFileForm, AddressForm, \
    DocumentForm, ReminderForm, RecoveryForm, SmsCautionForm, EmployeeFileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import EmployeeFile, DocumentFile, PhoneFile, FollowUp, FileReminder
from bank.models import File
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from bank.models import PersonFile
from django.contrib.auth.decorators import permission_required
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
            return HttpResponseRedirect('/employee/login')

    else:
            user_form = UserRegistrationForm()

    return render(request, 'bank/employee/register.html', {'form': user_form})


@login_required(login_url='/employee/login/')
@permission_required('employee.profile.dashboard')
def dashboard(request):
    files_emp = EmployeeFile.objects.filter(employee=request.user).values_list('file', flat=True)
    follows = FollowUp.objects.filter(file__in=files_emp)[:8]
    reminders = FileReminder.objects.filter(file__in=files_emp).order_by('-created_at')[:10]
    last_files = EmployeeFile.files.filter(employee=request.user).order_by('-created_at')[:10]

    return render(
        request,
        'bank/employee/dashboard.html',
        {
            'follows': follows,
            'reminders': reminders,
            'files': last_files
        }
    )


@login_required(login_url='/employee/login/')
def files(request):
    query = request.POST.get('q')
    if query:
        employee_files = EmployeeFile.files.filter(employee=request.user).filter(
            Q(file__file_code__contains=query) | Q(file__contract_code__contains=query))

    else:
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

        else:
            follow_form = FollowUpForm()
            # messages.add_message(request, messages.ERROR, 'خطا در ثبت پیگیری')

        if phone_form.is_valid():
            try:
                result_phone_form = phone_form.save(commit=False)
                result_phone_form.file = file
                result_phone_form.save()
                messages.add_message(request, messages.SUCCESS, 'شماره تماس با موفقیت ثبت شد')

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
                address_form = AddressForm()

        else:
            address_form = AddressForm()

        if document_form.is_valid():
            try:

                result_document_form = document_form.save(commit=False)
                result_document_form.file = file
                result_document_form.save()

            except:
                document_form = DocumentForm()

        else:
            print(document_form.errors)

        if reminder_form.is_valid():
            try:

                result_reminder_form = reminder_form.save(commit=False)
                result_reminder_form.file = file
                result_reminder_form.save()
                reminder_form = ReminderForm()
            except:
                reminder_form = ReminderForm()

        else:
            reminder_form = ReminderForm()

        if recovery_form.is_valid():
            try:
                result_recovery_form = recovery_form.save(commit=False)
                result_recovery_form.file = file
                result_recovery_form.save()
                recovery_form = RecoveryForm()

            except:
                recovery_form = RecoveryForm()

        if sms_form.is_valid():
            try:
                result_sms_form = sms_form.save(commit=False)
                result_sms_form.file = file
                result_sms_form.save()
                messages.add_message(request, messages.SUCCESS, 'پیامک با موفقیت ثبت شد')
                sms_form = SmsCautionForm()
                sms_form.fields['mobile_number'].queryset = PhoneFile.objects.filter(file=file)

            except:
                messages.add_message(request, messages.ERROR, 'هشدار پیامک تکراری است.')
                sms_form = SmsCautionForm()
                sms_form.fields['mobile_number'].queryset = PhoneFile.objects.filter(file=file)

        else:
            sms_form = SmsCautionForm()

    else:
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