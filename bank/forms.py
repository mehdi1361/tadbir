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


# class FileForm(forms.ModelForm):
#     class Meta:
#         model = File
#         fields = [
#             'file_code',
#             'contract_code',
#             'main_deposit',
#             'end_deposit',
#             'cost_proceeding',
#             'branch',
#             'persian_date_refrence'
#         ]
#         widgets = {
#             'branch': autocomplete.ModelSelect2(url='bank:branch-autocomplete')
#         }


class FileForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(FileForm, self).save(commit=False)
        instance.persian_normal_date_refrence = '1394'
        if commit:
            instance.save()
        return instance

    class Meta:
        model = File
        fields = [
            'file_code',
            'contract_code',
            'main_deposit',
            'nc_deposit',
            'so_deposit',
            'cost_proceeding',
            'branch',
            'persian_date_refrence',
            'status',
            'file_type'
        ]
        widgets = {
            'file_code': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_code': forms.TextInput(attrs={'class': 'form-control'}),
            'main_deposit': forms.TextInput(attrs={'class': 'form-control'}),
            'nc_deposit': forms.TextInput(attrs={'class': 'form-control'}),
            'so_deposit': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_proceeding': forms.TextInput(attrs={'class': 'form-control'}),
            'persian_date_refrence': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-control'}),
        }
