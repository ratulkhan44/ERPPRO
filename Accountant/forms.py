from django import forms
from Accountant.models import *
from People.models import *


class BaseAccountForm(forms.ModelForm):
    base_account = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'base_account'}))

    class Meta:
        model = BaseAccount
        fields = "__all__"


class AccountTypeForm(forms.ModelForm):

    base_account = forms.ModelChoiceField(queryset=BaseAccount.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control', 'id': 'base_account'}))
    account_type = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'account_type'}))

    class Meta:
        model = AccountType
        fields = "__all__"


class AccountForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(
    ), widget=forms.Select(attrs={'class': 'js-example-basic-single', 'id': 'account_type'}))
    account_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'account_name'}))
    account_code = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'account_code'}))
    total_debit = forms.DecimalField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'id': 'total_debit', 'value': 0.00}))
    total_credit = forms.DecimalField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'id': 'total_credit', 'value': 0.00}))
    description = forms.Textarea()

    class Meta:
        model = CreateAccount
        widgets = {
            "description": forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
        fields = "__all__"
