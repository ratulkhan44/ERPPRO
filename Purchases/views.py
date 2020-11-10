from django.shortcuts import render
from Accountant.models import *
from django.db.models import Q

# Create your views here.


def add_expense(request):
    # (baseAccount.objects.filter(Q(base_account__iexact=account) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
    #     start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
    paid_accounts = CreateAccount.objects.filter(
        Q(account_name__iexact='Cash') | Q(account_name__iexact='Bank A/C')).order_by('id')
    expense_accounts = CreateAccount.objects.filter(Q(account_type_id=7) | Q(account_type_id=8) | Q(account_type_id=9) | Q(
        account_type_id=10) | Q(account_type_id=11) | Q(account_type_id=12) | Q(account_type_id=13) | Q(account_type_id=14))
    peoples = People.objects.all()

    return render(request, 'purchases/add_expense.html', context={'expense_accounts': expense_accounts, 'paid_accounts': paid_accounts, 'peoples': peoples})
