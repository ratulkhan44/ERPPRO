from django.shortcuts import render,reverse,redirect
from . import forms
from .models import UserRole,CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from Expense.models import Expense
from django.db.models import Q

# Create your views here.

def user_role(request):
    form = forms.UserRoleForm()

    if request.method == 'POST':
        form = forms.UserRoleForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "User Role created successfully")
            return HttpResponseRedirect(reverse('User:user_role'))
    #roles = UserRole.objects.all()        
    return render(request,'user/role.html',context={'form':form})
    

def create_user(request):
    form = forms.CustomUserCretaionForm()

    if request.method == 'POST':
        
        form = forms.CustomUserCretaionForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            form.save(commit=True)
            form = forms.CustomUserCretaionForm()
                        
            messages.success(request, 'User successfully created')
            return HttpResponseRedirect(reverse('User:create_user'))

    return render(request,'user/create_user.html', context={'form':form})  

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # import pdb
        # pdb.set_trace()
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active and str(user.user_role)=='Accounts':
                login(request,user)
                return render(request,'user/roles/accounts/dashboard.html')
            elif user.is_active and str(user.user_role)=='Employee':
                login(request,user)
                return render(request,'user/roles/employee/dashboard.html') 
            elif user.is_active and str(user.user_role)=='Executive':
                login(request,user)
                return HttpResponseRedirect(reverse('User:executive_dashboard'))
            elif user.is_active and str(user.user_role)=='Supervisor':
                login(request,user)
                return HttpResponseRedirect(reverse('User:supervisor_dashboard'))          
            else:
                return HttpResponse('Account doesnt match')

        else:
            return HttpResponse("Username and password wrong")
    else:
        return render(request,'user/login.html') 

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('User:user_login'))

@login_required
def executive_dashboard(request):
    pending_expense=Expense.objects.filter(Q(is_supervisior=False) & Q(paid_account_id=32) ).count()
    expenses=Expense.objects.filter(Q(is_supervisior=False) & Q(paid_account_id=32))
    context={
        'expenses':expenses,
        'pending_expense':pending_expense
    }
    return render(request,'user/roles/executive/dashboard.html',context)

@login_required
def supervisor_dashboard(request):
    pending_expense=Expense.objects.filter(Q(is_supervisior=False) & Q(paid_account_id=32) ).count()
    expenses=Expense.objects.filter(Q(is_supervisior=False) & Q(paid_account_id=32))
    context={
        'expenses':expenses,
        'pending_expense':pending_expense
    }
    return render(request,'user/roles/supervisior/dashboard.html',context)    

@login_required
def supervisior_petty_cash_expense(request):
    expenses=Expense.objects.filter(Q(is_supervisior=False) & Q(paid_account_id=32))
    context={
        'expenses':expenses,
    }
    return render(request,'user/roles/supervisior/expense_pettycash.html',context)
@login_required
def supervisior_petty_cash_expense_accept(request,id):
    expense=Expense.objects.get(id=id)
    expense.is_supervisior=True
    expense.save()
    return HttpResponseRedirect(reverse('User:supervisior_petty_cash_expense'))


