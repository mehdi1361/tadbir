from django import forms
from django.contrib.auth.models import User

from .models import Profile, FollowUp, PhoneFile, AddressFile, \
    DocumentFile, FileReminder, FileRecovery, SmsCaution, EmployeeFile, EmployeePermission, AccessEmployee
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control text-input',
        'placeholder': 'نام کاربری',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control text-input',
            'placeholder': '********'
        }
    ))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={
            'class': 'form-control text-input',
            'placeholder': '********'
        }
    ))
    password2 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={
            'class': 'form-control text-input',
            'placeholder': '********'
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control text-input',
                'placeholder': 'ایمیل'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control text-input',
                'placeholder': 'نام کاربری'
            }),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password dont match')
        return cd['password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'father_name',
            'national_code',
            'certificate',
            'employee_post',
            'gender'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'national_code': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'certificate': forms.Select(attrs={'class': 'form-control'}),
            'employee_post': forms.Select(attrs={'class': 'form-control'}),
        }


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = [
            'follow_up_type',
            'description',
        ]
        widgets = {
            'follow_up_type': forms.Select(attrs={'class': 'form-control'}),
            # 'description': forms.Textarea(attrs={
            #     'class': 'form-control'
            # }),
        }


class PhoneFileForm(forms.ModelForm):
    class Meta:
        model = PhoneFile
        fields = [
            'phone_number',
            'phone_owner',
            'description'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'person_owner': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        objects = PhoneFile.objects.filter(
            file=cleaned_data.get('file'),
            phone_number=cleaned_data.get('phone_number')
        )

        if len(objects) > 0:
            msg = u"This row is not unique"
            raise ValidationError(msg)

        return cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressFile
        fields = [
            'address',
            'person_type',
            'type',
            'description'
        ]
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'person_type': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentFile
        fields = [
            'type',
            'description',
            'image_upload',
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }


class ReminderForm(forms.ModelForm):
    class Meta:
        model = FileReminder
        fields = [
            'subject',
            'detail',
            'persian_date'
        ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'persian_date': forms.TextInput(attrs={'id': 'persian_date'})
        }


class RecoveryForm(forms.ModelForm):
    class Meta:
        model = FileRecovery
        fields = [
            'recovery_type',
            'value',
            'value_code',
            'recovery_date',
            'detail'
        ]
        widgets = {
            'recovery_type': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'value_code': forms.TextInput(attrs={'class': 'form-control'}),
            'recovery_date': forms.TextInput(attrs={'id': 'recovery_date'}),
            'detail': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }


class SmsCautionForm(forms.ModelForm):
    class Meta:
        model = SmsCaution
        fields = [
            'type',
            'mobile_number',
            'description'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'mobile_number': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }


class EmployeeFileForm(forms.ModelForm):
    class Meta:
        model = EmployeeFile
        fields = [
            'status',
            'auth_status'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'auth_status': forms.Select(attrs={'class': 'form-control'})
        }


class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password'].label = 'رمز جدید'
        self.fields['repeat_new_password'].label ='تکرار رمز جدید'

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control text-input',
            'placeholder': '********'
        }
    ))
    repeat_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control text-input',
        'placeholder': '********'
    }
    ))


class UserCreationForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control text-input',
    }
    ))


class PermissionForm(forms.ModelForm):
    class Meta:
        model = EmployeePermission
        fields = [
            'enable'
        ]
        widgets = {
            'enable': forms.CheckboxInput()
        }


class EmpForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=EmployeePermission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

# class SearchForm(forms.Form):
#     text = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     file_code = forms.BooleanField(label='شماره پرونده', initial=False, required=False)
#     contract_code = forms.BooleanField(label='شماره قرارداد', initial=False, required=False)
#     name = forms.BooleanField(label='نام مدیون', initial=False, required=False)


class AccessAreaForm(forms.ModelForm):
    class Meta:
        model = AccessEmployee

        fields = [
            'area'
        ]
        widgets = {
            'area': forms.Select(attrs={'class': 'form-control'})
        }
