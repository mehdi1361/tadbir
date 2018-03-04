import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from employee.forms import PhoneFileForm, AddressForm, DocumentForm
from .models import Bank, ManagementAreas, Branch, File, Person, Office, SmsType, PersonFile
from django.views.generic import ListView
from .forms import BankForm, AreaForm, BranchForm, FileForm, \
    PersonForm, AssuranceForm, PersonFileForm, FileOfficeForm, SmsTypeForm, EmployeeFileForm, PersonOfficeForm, \
    OfficeForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import authenticate, login
# from .forms import LoginForm


@login_required(login_url='/employee/login/')
def bank_list(request):
    banks = Bank.objects.all()
    return render(request, 'bank/bank/list.html', {'banks': banks})


class BankListView(LoginRequiredMixin, ListView):
    login_url = '/employee/login/'
    queryset = Bank.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'bank/bank/list.html'


@login_required(login_url='/employee/login/')
def new_bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank:bank_list')

    else:
        form = BankForm(request.POST)

    return render(request, 'bank/bank/new.html', {'form': form})


@login_required(login_url='/employee/login/')
def edit_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:bank_list'))

    else:
        form = BankForm(request.POST)

    return render(request, 'bank/bank/edit.html', {'form': form, 'bank': bank})


@login_required(login_url='/employee/login/')
def management_area_list(request):
    areas = ManagementAreas.objects.all()
    return render(request, 'bank/management_area/list.html', {'areas': areas})


@login_required(login_url='/employee/login/')
def new_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:areas_list'))

    else:
        form = AreaForm(request.POST)

    return render(request, 'bank/management_area/new.html', {'form': form})


@login_required(login_url='/employee/login/')
def edit_area(request, area_id):
    area = get_object_or_404(ManagementAreas, id=area_id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:bank_list'))

    else:
        form = AreaForm(request.POST)

    return render(request, 'bank/bank/edit.html', {'form': form, 'area': area})


class BranchListView(LoginRequiredMixin, ListView):
    login_url = '/employee/login/'
    queryset = Branch.objects.all()
    context_object_name = 'branches'
    paginate_by = 3
    template_name = 'bank/branch/list.html'


@login_required(login_url='/employee/login/')
def new_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:branches_list'))

    else:
        form = BranchForm(request.POST)

    return render(request, 'bank/branch/new.html', {'form': form})


@login_required(login_url='/employee/login/')
def file_list(request):
    query = request.POST.get('q')
    if query:
        object_list = File.objects.filter(
            Q(file_code__contains=query) | Q(contract_code__contains=query)
        ).order_by('-created_at')
    else:
        object_list = File.objects.all().order_by('-created_at')
    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')

    try:
        files = paginator.page(page)

    except PageNotAnInteger:
        files = paginator.page(1)

    except EmptyPage:
        files = paginator.page(paginator.num_pages)

    return render(request, 'bank/file/list.html', {'files': files, 'page': page})


class BranchAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Branch.objects.all()

        if self.q:
            qs = qs.filter(name__contains=self.q)

        return qs


@login_required(login_url='/employee/login/')
def new_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:files_list'))
        else:
            print(form.errors)

    form = FileForm()

    return render(request, 'bank/file/new.html', {'form': form})


@login_required(login_url='/employee/login/')
def file_document(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        person_form = PersonFileForm(request.POST)
        person_office = FileOfficeForm(request.POST)
        assurance_form = AssuranceForm(request.POST)
        phone_form = PhoneFileForm(request.POST)
        phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)
        address_form = AddressForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES or None)
        employee_file_form = EmployeeFileForm(request.POST)

        if person_form.is_valid():
            new_person_file = person_form.save(commit=False)
            new_person_file.file = file
            new_person_file.save()

        if person_office.is_valid():
            new_office_file = person_office.save(commit=False)
            new_office_file.file = file
            new_office_file.save()

        if assurance_form.is_valid():
            new_assurance_file = assurance_form.save(commit=False)
            new_assurance_file.file = file
            new_assurance_file.save()

        if phone_form.is_valid():
            try:
                result_phone_form = phone_form.save(commit=False)
                result_phone_form.file = file
                result_phone_form.save()
                messages.add_message(request, messages.SUCCESS, 'شماره تماس با موفقیت ثبت شد')

            except:
                messages.add_message(request, messages.ERROR, 'هشدار شماره تلفن تکراری است.')

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
                messages.add_message(request, messages.SUCCESS, 'تصویر با موفقیت ثبت شد.')

            except:
                messages.add_message(request, messages.ERROR, 'مشکل در ثبت تضویر')

        if employee_file_form.is_valid():
            try:
                result_employee_file_form = employee_file_form.save(commit=False)
                result_employee_file_form.file = file
                result_employee_file_form.save()
                messages.add_message(request, messages.SUCCESS, 'تخصیص با موفقیت ثبت شد.')

            except:
                messages.add_message(request, messages.ERROR, 'خطا در ثبت')

        else:
            print(employee_file_form.errors)

    person_form = PersonFileForm()
    person_office = FileOfficeForm()
    assurance_form = AssuranceForm()
    phone_form = PhoneFileForm()
    phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)
    address_form = AddressForm()
    document_form = DocumentForm()
    employee_file_form = EmployeeFileForm()

    return render(
        request,
        'bank/file/file_detail.html',
        {
            'person_form': person_form,
            'person_office': person_office,
            'assurance_form': assurance_form,
            'file': file,
            'phone_form': phone_form,
            'address_form': address_form,
            'document_form': document_form,
            'employee_file_form': employee_file_form
        }
    )


@login_required(login_url='/employee/login/')
def get_branch(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        branches = Branch.objects.filter(name__contains=q)[:20]
        results = []
        for branch in branches:
            branch_json = {
                'id': branch.id,
                'label': str(branch),
                'value': str(branch)
            }
            results.append(branch_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required(login_url='/employee/login/')
def new_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'کاربر با موفقیت ذخیره شد.')
            form = PersonForm()

        else:
            messages.add_message(request, messages.WARNING, form.errors)
            form = PersonForm(request.POST)

    else:
        form = PersonForm()

    return render(
        request,
        'bank/person/new.html',
        {'form': form}
    )


@login_required(login_url='/employee/login/')
def get_persons(request):
    object_list = Person.objects.all().order_by('-created_at')
    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')

    try:
        persons = paginator.page(page)

    except PageNotAnInteger:
        persons = paginator.page(1)

    except EmptyPage:
        persons = paginator.page(paginator.num_pages)

    return render(request, 'bank/person/list.html', {'persons': persons, 'page': page})


@login_required(login_url='/employee/login/')
def new_person_office(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'شرکت با موفقیت ذخیره شد.')
            form = OfficeForm

        else:
            messages.add_message(request, messages.WARNING, form.errors)
            form = PersonOfficeForm(request.POST)

    else:
        form = OfficeForm()

    return render(
        request,
        'bank/person_office/new.html',
        {'form': form}
    )


@login_required(login_url='/login/')
def get_person_office(request):
    object_list = Office.objects.all().order_by('-created_at')
    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')

    try:
        persons_office = paginator.page(page)

    except PageNotAnInteger:
        persons_office = paginator.page(1)

    except EmptyPage:
        persons_office = paginator.page(paginator.num_pages)

    return render(request, 'bank/person_office/list.html', {'persons_office': persons_office, 'page': page})


@login_required(login_url='/employee/login/')
def sms_type_list(request):
    if request.method == 'POST':
        form = SmsTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'نوع پیامک با موفقیت ذخیره شد.')
            form = SmsTypeForm()

        else:
            messages.add_message(request, messages.WARNING, form.errors)
            form = SmsTypeForm(request.POST)

    else:
        form = SmsTypeForm()

    types = SmsType.objects.all()
    return render(request, 'bank/sms_type/list.html',
                  {'types': types,
                   'form': form}
                  )


def error_404(request):
    data = {}
    return render(request, 'bank/bank/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'bank/bank/500.html', data)
