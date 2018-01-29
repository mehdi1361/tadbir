from django import forms
from .models import Bank, ManagementAreas, Branch, File, Assurance, PersonFile, Person, Office, FileOffice
from dal import autocomplete
from django.forms.models import inlineformset_factory


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


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

        fields = [
            'first_name',
            'last_name',
            'father_name',
            'national_code',
            'gender'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'national_code': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


class PersonFileForm(forms.ModelForm):
    class Meta:
        model = PersonFile
        fields = [
            'file',
            'person',
            'relation_type'
        ]
        widgets = {
            'office': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.Select(attrs={'class': 'form-control'}),
            # 'file': forms.TextInput(attrs={'class': 'form-control'}),
            'relation_type': forms.Select(attrs={'class': 'form-control'}),
        }


class FileOfficeForm(forms.ModelForm):
    class Meta:
        model = FileOffice
        fields = [
            'file',
            'office',
            'relation_type'
        ]
        widgets = {
            'office': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.Select(attrs={'class': 'form-control'}),
            # 'file': forms.TextInput(attrs={'class': 'form-control'}),
            'relation_type': forms.Select(attrs={'class': 'form-control'}),
        }


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office

        fields = [
            'name',
            'register_number',
            'city',
            'address',
            'postal_code'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'register_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
inlineformset_factory(Person, PersonFile, form=PersonFileForm, extra=2)
