from django.shortcuts import render
from Accountant.models import CreateAccount

# Create your views here.


def opening_balance(request):
    asset_accounts = CreateAccount.objects.filter(
        account_type__base_account__base_account="Asset")
    expense_accounts = CreateAccount.objects.filter(
        account_type__base_account__base_account="Expenses")
    liability_accounts = CreateAccount.objects.filter(
        account_type__base_account__base_account="Liabilities")
    income_accounts = CreateAccount.objects.filter(
        account_type__base_account__base_account="Income")
    equity_accounts = CreateAccount.objects.filter(
        account_type__base_account__base_account="Equity")
    context = {
        'asset_accounts': asset_accounts,
        'expense_accounts': expense_accounts,
        'liability_accounts': liability_accounts,
        'income_accounts': income_accounts,
        'equity_accounts': equity_accounts
    }
    return render(request, 'settings/opening_balance.html', context)
