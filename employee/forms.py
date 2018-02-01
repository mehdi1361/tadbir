from django import forms
from django.contrib.auth.models import User


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
    password = forms.CharField(label='password')
    password2 = forms.CharField(label='password')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password dont match')
        return cd['password2']
