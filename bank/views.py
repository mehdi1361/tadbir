import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from employee.forms import PhoneFileForm, AddressForm, DocumentForm
from employee.models import EmployeePermission, PhoneFile, AddressFile
from .models import Bank, ManagementAreas, Branch, File, Person, Office, SmsType, PersonFile, FileOffice, Lawyer, \
    FollowLawType, FollowInLowFile, Assurance
from django.views.generic import ListView
from .forms import BankForm, AreaForm, BranchForm, FileForm, PersonForm, AssuranceForm, PersonFileForm, FileOfficeForm, \
    SmsTypeForm, EmployeeFileForm, PersonOfficeForm, OfficeForm, LawyerForm, LawyerFileForm, FollowLawTypeForm, \
    SearchForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from common.decorators import employee_permission
from common.utils import normalize_data
from django.forms import inlineformset_factory


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
@employee_permission('bank_new')
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
@employee_permission('bank_list')
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
@employee_permission('area_list')
def management_area_list(request):
    areas = ManagementAreas.objects.all()
    return render(request, 'bank/management_area/list.html', {'areas': areas})


@login_required(login_url='/employee/login/')
@employee_permission('area_new')
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
@employee_permission('area_edit')
def edit_area(request, area_id):
    area = get_object_or_404(ManagementAreas, id=area_id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:areas_list'))

    form = AreaForm(instance=area)

    return render(request, 'bank/bank/edit.html', {'form': form, 'area': area})


# @employee_permission('branch_list')
class BranchListView(LoginRequiredMixin, ListView):
    login_url = '/employee/login/'
    queryset = Branch.objects.all()
    context_object_name = 'branches'
    # paginate_by = 10
    template_name = 'bank/branch/list.html'


@login_required(login_url='/employee/login/')
@employee_permission('branch_new')
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
@employee_permission('branch_edit')
def edit_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:branches_list'))

    form = BranchForm(instance=branch)

    return render(request, 'bank/branch/new.html', {'form': form})


@login_required(login_url='/employee/login/')
@employee_permission('file_list')
def file_list(request):
    object_list = File.ordered.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            query = cd['text']
            query = normalize_data(query)

            person_file = PersonFile.objects.filter(
                person__name__contains=query).values_list('file__file_code', flat=True)

            office_files = FileOffice.objects.filter(
                office__name__contains=query).values_list('file__file_code', flat=True)

            if cd['name'] and cd['file_code'] and cd['contract_code']:
                object_list = File.ordered.filter(
                    Q(file_code__contains=query) | Q(contract_code__contains=query)
                    | Q(file_code__in=person_file) | Q(file_code__in=office_files)
                ).order_by('-created_at')

            elif cd['name'] and cd['file_code'] and not cd['contract_code']:
                object_list = File.ordered.filter(
                    Q(file_code__contains=query) | Q(file_code__in=person_file) |
                    Q(file_code__in=office_files)
                ).order_by('-created_at')

            elif cd['name'] and not cd['file_code'] and cd['contract_code']:
                object_list = File.ordered.filter(
                    Q(contract_code__contains=query) | Q(file_code__in=person_file) |
                    Q(file_code__in=office_files)
                ).order_by('-created_at')

            elif cd['name'] and not cd['file_code'] and not cd['contract_code']:
                object_list = File.ordered.filter(Q(file_code__in=person_file) | Q(file_code__in=office_files)
                                                  ).order_by('-created_at')

            elif not cd['name'] and cd['file_code'] and cd['contract_code']:
                object_list = File.ordered.filter(Q(contract_code__contains=query)
                                                  | Q(file_code__in=person_file)).order_by('-created_at')

            elif not cd['name'] and cd['file_code'] and not cd['contract_code']:
                object_list = File.ordered.filter(file_code__contains=query).order_by('-created_at')

            elif not cd['name'] and not cd['file_code'] and cd['contract_code']:
                object_list = File.ordered.filter(contract_code__contains=query).order_by('-created_at')

            else:
                object_list = File.ordered.all()
                form = SearchForm()

        else:
            object_list = File.ordered.all()
            form = SearchForm()

    else:
        object_list = File.ordered.all()
        form = SearchForm()

    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')

    try:
        files = paginator.page(page)

    except PageNotAnInteger:
        files = paginator.page(1)

    except EmptyPage:
        files = paginator.page(paginator.num_pages)

    return render(request, 'bank/file/list.html', {'files': files, 'page': page, 'form': form})


class BranchAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Branch.objects.all()

        if self.q:
            qs = qs.filter(name__contains=self.q)

        return qs


@login_required(login_url='/employee/login/')
@employee_permission('file_new')
def new_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:files_list'))
        else:
           pass 

    form = FileForm()

    return render(request, 'bank/file/new.html', {'form': form})


@login_required(login_url='/employee/login/')
@employee_permission('file_new')
def file_document(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    follow_law_formset = inlineformset_factory(File, FollowInLowFile, fields=('enable', 'follow'))

    formset = follow_law_formset(instance=file)
    if request.method == 'POST':
        person_form = PersonFileForm(request.POST)
        person_office = FileOfficeForm(request.POST)
        assurance_form = AssuranceForm(request.POST)
        phone_form = PhoneFileForm(request.POST)
        phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)
        address_form = AddressForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES or None)
        employee_file_form = EmployeeFileForm(request.POST)
        lawyer_form = LawyerFileForm(request.POST)
        file_detail = FileForm(request.POST, instance=file)

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

        if lawyer_form.is_valid():
            result_lawyer = lawyer_form.save(commit=False)
            result_lawyer.file = file
            result_lawyer.save()

        if file_detail.is_valid():
            result_file_detail = file_detail.save(commit=False)
            result_file_detail.file = file
            result_file_detail.save()

    person_form = PersonFileForm()
    person_office = FileOfficeForm()
    assurance_form = AssuranceForm()
    phone_form = PhoneFileForm()
    phone_form.fields['phone_owner'].queryset = PersonFile.objects.filter(file=file)
    address_form = AddressForm()
    document_form = DocumentForm()
    employee_file_form = EmployeeFileForm()
    lawyer_form = LawyerFileForm()
    file_detail = FileForm(instance=file)

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
            'lawyer_form': lawyer_form,
            'employee_file_form': employee_file_form,
            'law_formset': formset,
            'file_detail': file_detail
        }
    )


@login_required(login_url='/employee/login/')
@employee_permission('branch_list')
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
@employee_permission('employee_file')
def new_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'شخص حقیقی با موفقیت ذخیره شد.')
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
    query = request.POST.get('q')
    if query:
        normalize_data(query)
        object_list = Person.objects.filter(name__contains=query).order_by('-created_at')
    else:
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
    query = request.POST.get('q')
    if query:
        normalize_data(query)
        object_list = Office.objects.filter(name__contains=query).order_by('-created_at')

    else:
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
@employee_permission('sms_list')
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


@login_required(login_url='/employee/login/')
@employee_permission('set_permission')
def set_permission(request):
    all_user = User.objects.all()
    query = request.POST.get('q')
    if query:
        selected_user = User.objects.get(username=query)
        permissions = EmployeePermission.objects.filter(employee=selected_user)
        return render(request, 'bank/permissions/list.html', {
            'selected_user': selected_user,
            'permissions': permissions,
            'users': all_user
        })

    return render(request, 'bank/permissions/list.html', {'users': all_user})


@login_required(login_url='/employee/login/')
@employee_permission('person_edit')
def edit_person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person_form = PersonFileForm(request.POST, instance=person)

    if request.method == 'POST':
        if person_form.is_valid():
            person_form.save()

        else:
            messages.add_message(request, messages.ERROR, 'خطا در بروز رسانی')
            person_form = PersonFileForm(instance=person)

    else:
        person_form = PersonFileForm(instance=person)

    return render(request, 'bank/file/edit_person.html', {'form': person_form})


@login_required(login_url='/employee/login/')
def get_lawyers(request):
    query = request.POST.get('q')
    if query:
        normalize_data(query)
        object_list = Lawyer.objects.filter(name__contains=query).order_by('-created_at')
    else:
        object_list = Lawyer.objects.all().order_by('-created_at')

    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')

    try:
        lawyers = paginator.page(page)

    except PageNotAnInteger:
        lawyers = paginator.page(1)

    except EmptyPage:
        lawyers = paginator.page(paginator.num_pages)

    return render(request, 'bank/lawyer/list.html', {'lawyers': lawyers, 'page': page})


@login_required(login_url='/employee/login/')
@employee_permission('file_new')
def new_lawyer(request):
    if request.method == 'POST':
        form = LawyerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:get_lawyers'))
        else:
            print(form.errors)

    form = LawyerForm()

    return render(request, 'bank/lawyer/new.html', {'form': form})


@login_required(login_url='/employee/login/')
@employee_permission('file_new')
def follow_law(request):
    if request.method == 'POST':
        form = FollowLawTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:follow_in_law'))
        else:
            print(form.errors)

    form = FollowLawTypeForm()
    follow_laws = FollowLawType.objects.all()

    return render(request, 'bank/follow_low/follow_type_list.html',
                  {
                      'form': form,
                      'follow_laws': follow_laws
                  })


@login_required(login_url='/employee/login/')
# @employee_permission('file_new')
def delete_person_file(request, file_person_id):
    # person_file = PersonFile.objects.get(person_id=person_id, file_id=file_id)
    person_file = get_object_or_404(PersonFile, id=file_person_id)
    file_id = person_file.file.id
    person_file.delete()
    return redirect('bank:file_detail', file_id=file_id)


@login_required(login_url='/employee/login/')
# @employee_permission('file_new')
def delete_office_file(request, file_office_id):
    # person_file = PersonFile.objects.get(person_id=person_id, file_id=file_id)
    office_file = get_object_or_404(FileOffice, id=file_office_id)
    file_id = office_file.file.id
    office_file.delete()
    return redirect('bank:file_detail', file_id=file_id)


@login_required(login_url='/employee/login/')
# @employee_permission('file_new')
def delete_assurance(request, assurance_id):
    assurance_file = get_object_or_404(Assurance, id=assurance_id)
    file_id = assurance_file.file.id
    assurance_file.delete()
    return redirect('bank:file_detail', file_id=file_id)


@login_required(login_url='/employee/login/')
# @employee_permission('file_new')
def delete_phone(request, phone_id):
    phone_file = get_object_or_404(PhoneFile, id=phone_id)
    file_id = phone_file.file.id
    phone_file.delete()
    return redirect('bank:file_detail', file_id=file_id)


@login_required(login_url='/employee/login/')
# @employee_permission('file_new')
def delete_address(request, address_id):
    address_file = get_object_or_404(AddressFile, id=address_id)
    file_id = address_file.file.id
    address_file.delete()
    return redirect('bank:file_detail', file_id=file_id)
