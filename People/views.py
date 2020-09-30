from django.shortcuts import render, HttpResponseRedirect
from People.models import *
from People import forms
from django.contrib import messages
from django.urls import reverse

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


def people_list(request):
    peoples = People.objects.all()
    return render(request, 'people/people_list.html', context={'peoples': peoples})


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
