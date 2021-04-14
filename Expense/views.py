from django.shortcuts import render
from Accountant.models import *
from django.db.models import Q
import json
from django.contrib import messages
from .models import Expense
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

# Create your views here.

from django.contrib.auth.decorators import permission_required


# @permission_required('Expense.Can add expense')
def new_expense(request):
    paid_accounts = CreateAccount.objects.filter(
        Q(account_name__iexact='Cash') | Q(account_name__iexact='Bank A/C') | Q(account_name__iexact='Petty Cash')).order_by('id')
    expense_accounts = CreateAccount.objects.filter(Q(account_type_id=7) | Q(account_type_id=8) | Q(account_type_id=9) | Q(
        account_type_id=10) | Q(account_type_id=11) | Q(account_type_id=12) | Q(account_type_id=13) | Q(account_type_id=14))
    peoples = People.objects.all()

    if request.method == "POST":
        expense_date = request.POST.get('expense_date')
        paid_account = request.POST.get('paid_account')
        expense_account = request.POST.get('expense_account')
        particular = request.POST.get('particular')
        people_for = request.POST.get('people_for')
        people_by = request.POST.get('people_by')
        expense_image = request.FILES['expense_image']
        amount = request.POST.get('amount')
        user_id = request.user.id

        Expense.objects.create(expense_date=expense_date, paid_account_id=paid_account, expense_account_id=expense_account, particular=particular,
                               people_for_id=people_for, people_by_id=people_by, expense_image=expense_image, amount=amount, user_id=user_id)
        messages.success(request, 'Expense Created Successfully')
        return render(request, 'expense/new_expense.html', context={'expense_accounts': expense_accounts, 'paid_accounts': paid_accounts, 'peoples': peoples})

    return render(request, 'expense/new_expense.html', context={'expense_accounts': expense_accounts, 'paid_accounts': paid_accounts, 'peoples': peoples})


def all_expense(request):
    expenses = Expense.objects.all()
    return render(request, 'expense/all_expense.html', context={'expenses': expenses, })


def new_recurring_expense(request):
    paid_accounts = CreateAccount.objects.filter(
        Q(account_name__iexact='Cash') | Q(account_name__iexact='Bank A/C') | Q(account_name__iexact='Petty Cash')).order_by('id')
    expense_accounts = CreateAccount.objects.filter(Q(account_type_id=7) | Q(account_type_id=8) | Q(account_type_id=9) | Q(
        account_type_id=10) | Q(account_type_id=11) | Q(account_type_id=12) | Q(account_type_id=13) | Q(account_type_id=14))
    # expense_accounts = AccountType.objects.filter(
    #     base_account__base_account="Income")
    peoples = People.objects.all()
    return render(request, 'expense/recurring_expense.html', context={'expense_accounts': expense_accounts, 'paid_accounts': paid_accounts, 'peoples': peoples})
