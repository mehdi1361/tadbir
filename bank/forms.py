from django import forms
from .models import Bank, ManagementAreas, Branch, File
from dal import autocomplete


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = ManagementAreas
        fields = ['name', 'postal_code', 'address', 'state', 'bank']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'area', 'city', 'address', 'postal_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'file_code',
            'contract_code',
            'main_deposit',
            'end_deposit',
            'cost_proceeding',
            'branch',
            'persian_date_refrence'
        ]
        widgets = {
            'branch': autocomplete.ModelSelect2(url='branch-autocomplete')
        }
