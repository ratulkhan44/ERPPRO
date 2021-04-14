from django import forms
from .models import Vendor


class VendorForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'name'}))
    company = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'company'}))
    department = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'department'}))
    designation = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'designation'}))
    contact = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'contact'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'email'}))
    website = forms.URLField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'website'}))
    opening_balance = forms.DecimalField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'opening_balance'}))
    address = forms.Textarea()

    class Meta:
        model = Vendor
        widgets = {
            "address": forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
        fields = "__all__"
