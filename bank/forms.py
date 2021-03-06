from django import forms
from unidecode import unidecode
from employee.models import EmployeeFile
from .models import Bank, ManagementAreas, Branch, \
    File, Assurance, PersonFile, Person, Office, FileOffice, SmsType, Lawyer, LawyerFile, FollowLawType, FollowInLowFile

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
        fields = ['name', 'postal_code', 'address', 'state', 'bank', 'status']
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


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.fullname


class FileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['branch'].queryset = Branch.objects.all().order_by('area')

    def save(self, commit=True):
        instance = super(FileForm, self).save(commit=False)
        instance.persian_normal_date_refrence = '1394'
        if commit:
            instance.save()
        return instance

    def clean(self):
        data = self.cleaned_data
        if 'file_code' in data.keys() and data['file_code'] is not None:
            data['file_code'] = unidecode(data.get('file_code'))

        if 'contract_code' in data.keys() and data['contract_code'] is not None:
            data['contract_code'] = unidecode(data.get('contract_code'))

        if 'main_deposit' in data.keys() and data['main_deposit'] is not None:
            data['main_deposit'] = int(unidecode(str(data.get('main_deposit'))))

        if 'nc_deposit' in data.keys() and data['nc_deposit'] is not None:
            data['nc_deposit'] = int(unidecode(str(data.get('nc_deposit'))))

        if 'so_deposit' in data.keys() and data['so_deposit'] is not None:
            data['so_deposit'] = int(unidecode(str(data.get('so_deposit'))))

        if 'cost_proceeding' in data.keys() and data['cost_proceeding'] is not None:
            data['cost_proceeding'] = int(unidecode(str(data.get('cost_proceeding'))))

        if 'persian_date_refrence' in data.keys() and data['persian_date_refrence'] is not None:
            data['persian_date_refrence'] = unidecode(data.get('persian_date_refrence'))

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
            'persian_date_refrence': forms.TextInput(attrs={'id': 'date_input'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            # 'branch': CustomModelChoiceField(queryset=Branch.objects.all()),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-control'}),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

        fields = [
            'name',
            'father_name',
            'national_code',
            'gender'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'national_code': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


class PersonFileForm(forms.ModelForm):
    class Meta:
        model = PersonFile
        fields = [
            'person',
            'relation_type'
        ]
        widgets = {
            'person': forms.Select(attrs={'class': 'form-control'}),
            # 'file': forms.Select(attrs={'class': 'form-control'}),
            # 'file': forms.TextInput(attrs={'class': 'form-control'}),
            'relation_type': forms.Select(attrs={'class': 'form-control'}),
        }


class FileOfficeForm(forms.ModelForm):
    class Meta:
        model = FileOffice
        fields = [
            # 'file',
            'office',
            'relation_type'
        ]
        widgets = {
            'office': forms.Select(attrs={'class': 'form-control'}),
            # 'file': forms.Select(attrs={'class': 'form-control'}),
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


class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance

        fields = [
            # 'file',
            'assurance_type',
            'assurance_number',
            'assurance_value',
            'description'
        ]
        widgets = {
            # 'file': forms.Select(attrs={'class': 'form-control'}),
            'assurance_type': forms.Select(attrs={'class': 'form-control'}),
            'assurance_number': forms.TextInput(attrs={'class': 'form-control'}),
            'assurance_value': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),

        }


class SmsTypeForm(forms.ModelForm):
    class Meta:
        model = SmsType

        fields = [
            'subject',
            'detail',
        ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),

        }


class EmployeeFileForm(forms.ModelForm):
    class Meta:
        model = EmployeeFile
        fields = [
            'status',
            'auth_status',
            'employee'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'auth_status': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'})
        }


class PersonOfficeForm(forms.ModelForm):
    class Meta:
        model = FileOffice
        fields = [
            'office',
            'relation_type',
            'description'
        ]
        widgets = {
            'office': forms.Select(attrs={'class': 'form-control'}),
            'relation_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Select(attrs={'class': 'form-control'})
        }


class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer

        fields = [
            'name',
            'father_name',
            'mobile_number',
            'national_code',
            'gender'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'national_code': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


class LawyerFileForm(forms.ModelForm):
    class Meta:
        model = LawyerFile
        fields = [
            'lawyer'
        ]
        widgets = {
            # 'file': forms.Select(attrs={'class': 'form-control'}),
            'lawyer': forms.Select(attrs={'class': 'form-control'}),
        }


class FollowLawTypeForm(forms.ModelForm):
    class Meta:
        model = FollowLawType
        fields = [
            'type'
        ]
        widgets = {
            # 'file': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'})
        }


class FollowInLowFileForm(forms.ModelForm):
    class Meta:
        model = FollowInLowFile
        fields = [
            'follow',
            'enable'
        ]
        widgets = {
            # 'file': forms.Select(attrs={'class': 'form-control'}),
            'follow': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        }


class SearchForm(forms.Form):
    text = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    file_code = forms.BooleanField(label='شماره پرونده', initial=False, required=False)
    contract_code = forms.BooleanField(label='شماره قرارداد', initial=False, required=False)
    name = forms.BooleanField(label='نام مدیون', initial=False, required=False)


inlineformset_factory(Person, PersonFile, form=PersonFileForm, extra=2)
