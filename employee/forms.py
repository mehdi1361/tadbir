from django import forms
from django.contrib.auth.models import User
from .models import Profile, FollowUp, PhoneFile, AddressFile, DocumentFile, FileReminder
from ckeditor.widgets import CKEditorWidget
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
            'first_name',
            'last_name',
            'father_name',
            'national_code',
            'gender'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'national_code': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
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
            'person_type',
            'type',
            'description'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'person_type': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
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


# class ReminderForm(forms.ModelForm):
#     class Meta:
#         model = DocumentFile
#         fields = [
#             'type',
#             'description',
#             'image_upload',
#         ]
#         widgets = {
#             'type': forms.Select(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={
#                 'class': 'form-control'
#             })
#         }