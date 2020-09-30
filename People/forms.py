from django import forms
from People.models import *


class CompanyForm(forms.ModelForm):
    company_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'company_name'}))
    contact = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'contact'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'email'}))
    address = forms.Textarea()

    class Meta:
        model = Company
        widgets = {
            "address": forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
        fields = "__all__"


class DepartmentForm(forms.ModelForm):
    company_name = forms.ModelChoiceField(queryset=Company.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control', 'id': 'company_name'}))
    department_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'department_name'}))

    class Meta:
        model = Department
        fields = "__all__"


class PeopleForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'name'}))
    company = forms.ModelChoiceField(queryset=Company.objects.all(
    ), required=False, widget=forms.Select(attrs={'class': 'form-control company', 'id': 'company_name'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(
    ), required=False, widget=forms.Select(attrs={'class': 'form-control', 'id': 'department_name'}))
    contact = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'contact'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'email'}))
    blood_group = forms.ChoiceField(required=False, choices=BLOOD_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'blood_group'}))
    dob = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'type': 'date', 'class': 'form-control', 'id': 'dob'}))
    marital_status = forms.ChoiceField(required=False, choices=MARITAL_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'marital_status'}))
    nid = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'nid'}))
    passport = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'passport'}))
    tracking = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'tracking'}))
    address = forms.Textarea()

    class Meta:
        model = People
        widgets = {
            "address": forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
        fields = "__all__"
