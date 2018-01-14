from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Bank, ManagementAreas, Branch, File
from django.views.generic import ListView
from .forms import BankForm, AreaForm, BranchForm, FileForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dal import autocomplete


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
    object_list = File.objects.all()
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
            qs = qs.filter(name__isstartwith=self.q)

        return qs


def new_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('bank:files_list'))

    else:
        form = FileForm(request.POST)

    return render(request, 'bank/file/new.html', {'form': form})
