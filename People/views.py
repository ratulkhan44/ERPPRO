from django.shortcuts import render, HttpResponseRedirect
from People.models import *
from django.views import View
from People import forms
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
import json
from validate_email import validate_email
from django.contrib.auth.models import User
from django.core import serializers
# Create your views here.


def company_list(request):
    form = forms.CompanyForm()

    if request.method == 'POST':
        form = forms.CompanyForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Company Created Successfully')
            return HttpResponseRedirect(reverse('People:company_list'))
    companies = Company.objects.all()

    return render(request, 'people/company.html', context={'form': form, 'companies': companies})


def department_list(request):
    form = forms.DepartmentForm()

    if request.method == 'POST':
        form = forms.DepartmentForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Department Created Successfully')
            return HttpResponseRedirect(reverse('People:department_list'))
    departments = Department.objects.all()

    return render(request, 'people/department.html', context={'form': form, 'departments': departments})


def show_department(request,id):
    departments = list(Department.objects.filter(company_name_id=id))
    a=serializers.serialize('json', departments)
    return HttpResponse(a, content_type='application/json')


def people_list(request):
    peoples = People.objects.all()
    return render(request, 'people/people_list.html', context={'peoples': peoples})

class ContactValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        contact=data['contact']
        if len(contact)!=11:
            return JsonResponse({'contact_error':'Sorry! Contact number should be 11 digit only'},status=409)

        if People.objects.filter(contact=contact):
            return JsonResponse({'contact_error':'Sorry! Contact number already exist,Choose another number'},status=409)    

        return JsonResponse({'contact_valid':True})

class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['name']
        username.replace(" ", "")
        if not str(username.replace(" ", "")).isalnum():
            return JsonResponse({'name_error':'User name should be AlphaNumeric'},status=400)
        if People.objects.filter(name=username):
            return JsonResponse({'name_error':'Sorry! User name already exist,Choose another name'},status=409)    

        return JsonResponse({'username_valid':True}) 


class NidValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        nid=data['nid']
        
        if People.objects.filter(nid=nid):
            return JsonResponse({'nid_error':'Sorry! NID already exist,Choose another one'},status=409)    

        return JsonResponse({'nid_valid':True})     


class PassportValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        passport=data['passport']
        
        if People.objects.filter(passport=passport):
            return JsonResponse({'passport_error':'Sorry! Passport number already exist,Choose another one'},status=409)    

        return JsonResponse({'passport_valid':True})

class TrackingValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        tracking=data['tracking']
        
        if People.objects.filter(tracking=tracking):
            return JsonResponse({'tracking_error':'Sorry! tracking number already exist,Choose another one'},status=409)    

        return JsonResponse({'tracking_valid':True})


class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if People.objects.filter(email=email):
            return JsonResponse({'email_error':'Sorry! Email already exists,Choose another one'},status=409)    

        return JsonResponse({'email_valid':True})            


def create_people(request):
    form = forms.PeopleForm

    if request.method == 'POST':
        form = forms.PeopleForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'People Created Successfully')
            
            return HttpResponseRedirect(reverse('People:create_people'))
            

    return render(request, 'people/create_people.html', context={'form': form})


# def base_account(request):
#     form = forms.BaseAccountForm()

#     if request.method == 'POST':
#         form = forms.BaseAccountForm(request.POST)

#         if form.is_valid():
#             form.save(commit=True)
#             messages.success(request, 'Base Account Created Successfully')
#             return HttpResponseRedirect(reverse('Accountant:base_account'))

#     return render(request, 'accountant/base_account.html', context={'form': form})


# def showDepartment(request, pk):
#     department = Department.objects.get(id=pk)
#     return department
