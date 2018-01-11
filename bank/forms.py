from django import forms
from .models import Bank, ManagementAreas, Branch


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
