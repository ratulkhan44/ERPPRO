from django.shortcuts import render
from Accountant.models import ManualJournal, CreateAccount, AccountType, BaseAccount
from People.models import *
from django.db.models import Count
from django.db.models import Sum

# Create your views here.


def allreports(request):
    return render(request, 'reports/allreports.html', context={})


def general_ledger(request):
    accounts = CreateAccount.objects.all().order_by('account_name')

    #journal_accounts = ManualJournal.objects.all()
    return render(request, 'reports/general_ledger.html', context={'accounts': accounts})


def journal_report(request):
    # journals = ManualJournal.objects.order_by('voucher_no').values(
    # 'voucher_no', 'debit', 'credit').annotate(dcount = Count('voucher_no'))
    journals = ManualJournal.objects.all()
    return render(request, 'reports/journal_report.html', context={'journals': journals})


def account_transactions(request, id):
    accounts = ManualJournal.objects.filter(account_id=id)
    account_name = CreateAccount.objects.get(id=id)
    # a = AccountType.objects.filter(id=1).aggregate(
    # sum_total=Sum('createaccount_account_type__total_credit'))
    asset_debit = BaseAccount.objects.filter(id=2).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    # print(a)
    #abc = a.createaccount_account_type.all()
    return render(request, 'reports/account_transactions.html', context={'accounts': accounts, 'account_name': account_name})


def balance_sheet(request):
    asset_debit = BaseAccount.objects.filter(id=1).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    asset_credit = BaseAccount.objects.filter(id=1).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))
    current_asset_credit = AccountType.objects.filter(id=2).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    current_asset_debit = AccountType.objects.filter(id=2).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    fixed_asset_credit = AccountType.objects.filter(id=1).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    fixed_asset_debit = AccountType.objects.filter(id=1).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    current_asset_debit = AccountType.objects.filter(id=1).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    expense_debit = BaseAccount.objects.filter(id=2).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    expense_credit = BaseAccount.objects.filter(id=2).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))
    equity_debit = BaseAccount.objects.filter(id=5).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    equity_credit = BaseAccount.objects.filter(id=5).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))

    return render(request, 'reports/balance_sheet.html', context={'asset_debit': asset_debit, 'asset_credit': asset_credit, 'expense_debit': expense_debit, 'expense_credit': expense_credit, 'current_asset_credit': current_asset_credit, 'current_asset_debit': current_asset_debit, 'fixed_asset_credit': fixed_asset_credit, 'fixed_asset_debit': fixed_asset_debit, 'equity_debit': equity_debit, 'equity_credit': equity_credit})
