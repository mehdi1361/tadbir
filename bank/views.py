import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Bank, ManagementAreas, Branch, File, Person, PersonOffice
from django.views.generic import ListView
from .forms import BankForm, AreaForm, BranchForm, FileForm, PersonForm, PersonOfficeForm, PersonFileForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dal import autocomplete
from django.contrib import messages


def bank_list(request):
    banks = Bank.objects.all()
    return render(request, 'bank/bank/list.html', {'banks': banks})


class BankListView(ListView):
    queryset = Bank.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'bank/bank/list.html'


def new_bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:bank_list'))

    else:
        form = BankForm(request.POST)

    return render(request, 'bank/bank/new.html', {'form': form})


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


def management_area_list(request):
    areas = ManagementAreas.objects.all()
    return render(request, 'bank/management_area/list.html', {'areas': areas})


def new_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:area_list'))

    else:
        form = AreaForm(request.POST)

    return render(request, 'bank/management_area/new.html', {'form': form})


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


class BranchListView(ListView):
    queryset = Branch.objects.all()
    context_object_name = 'branches'
    paginate_by = 3
    template_name = 'bank/branch/list.html'


def new_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:branches_list'))

    else:
        form = BranchForm(request.POST)

    return render(request, 'bank/branch/new.html', {'form': form})


def file_list(request):
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


def new_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:new_file_detail'))

    else:
        form = FileForm(request.POST)

    return render(request, 'bank/file/new.html', {'form': form})


def file_document(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        person_form = PersonFileForm(request.POST)
        if person_form.is_valid():
            person_form.save()
    else:
        person_form = PersonFileForm(request.POST)

    return render(
        request,
        'bank/file/file_detail.html',
        {'person_form': person_form, 'file': file}
    )


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


def new_person_office(request):
    if request.method == 'POST':
        form = PersonOfficeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'شرکت با موفقیت ذخیره شد.')
            form = PersonOfficeForm

        else:
            messages.add_message(request, messages.WARNING, form.errors)
            form = PersonOfficeForm(request.POST)

    else:
        form = PersonOfficeForm()

    return render(
        request,
        'bank/person_office/new.html',
        {'form': form}
    )


def get_person_office(request):
    object_list = PersonOffice.objects.all().order_by('-created_at')
    paginator = Paginator(object_list, 15)
    page = request.GET.get('page')

    try:
        persons_office = paginator.page(page)

    except PageNotAnInteger:
        persons_office = paginator.page(1)

    except EmptyPage:
        persons_office = paginator.page(paginator.num_pages)

    return render(request, 'bank/person_office/list.html', {'persons_office': persons_office, 'page': page})