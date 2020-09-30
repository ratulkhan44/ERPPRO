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
    #account_name = CreateAccount.objects.get(id=id)
    # a = AccountType.objects.filter(id=1).aggregate(
    # sum_total=Sum('createaccount_account_type__total_credit'))
    # asset_debit = BaseAccount.objects.filter(id=2).aggregate(
    # sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    # print(a)
    #abc = a.createaccount_account_type.all()
    return render(request, 'reports/account_transactions.html', context={'accounts': accounts})


def balance_sheet(request):
    asset_debit = BaseAccount.objects.filter(id=1).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    asset_credit = BaseAccount.objects.filter(id=1).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))
    # current_asset_credit = AccountType.objects.filter(id=2).aggregate(
    #     sum_total=Sum('createaccount_account_type__total_credit'))
    # current_asset_debit = AccountType.objects.filter(id=2).aggregate(
    #     sum_total=Sum('createaccount_account_type__total_debit'))
    # fixed_asset_credit = AccountType.objects.filter(id=1).aggregate(
    #     sum_total=Sum('createaccount_account_type__total_credit'))
    # fixed_asset_debit = AccountType.objects.filter(id=1).aggregate(
    #     sum_total=Sum('createaccount_account_type__total_debit'))
    # current_asset_debit = AccountType.objects.filter(id=1).aggregate(
    #     sum_total=Sum('createaccount_account_type__total_debit'))
    # expense_debit = BaseAccount.objects.filter(id=2).aggregate(
    #     sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    # expense_credit = BaseAccount.objects.filter(id=2).aggregate(
    #     sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))
    equity_debit = BaseAccount.objects.filter(id=3).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    equity_credit = BaseAccount.objects.filter(id=3).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))

    liabilty_debit = BaseAccount.objects.filter(id=2).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    liabilty_credit = BaseAccount.objects.filter(id=2).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))

    return render(request, 'reports/balance_sheet.html', context={'asset_debit': asset_debit, 'asset_credit': asset_credit, 'equity_debit': equity_debit, 'equity_credit': equity_credit, 'liabilty_debit': liabilty_debit, 'liabilty_credit': liabilty_credit})


def trial_balance(request):
    current_asset_credit = AccountType.objects.filter(id=2).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    current_asset_debit = AccountType.objects.filter(id=2).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    fixed_asset_credit = AccountType.objects.filter(id=1).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    fixed_asset_debit = AccountType.objects.filter(id=1).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))

    current_liabilities_debit = AccountType.objects.filter(id=3).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    current_liabilities_credit = AccountType.objects.filter(id=3).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    capital_debit = AccountType.objects.filter(id=4).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    capital_credit = AccountType.objects.filter(id=4).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    sales_revenue_debit = AccountType.objects.filter(id=5).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    sales_revenue_credit = AccountType.objects.filter(id=5).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    misc_income_debit = AccountType.objects.filter(id=6).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    misc_income_credit = AccountType.objects.filter(id=6).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    cogs_debit = AccountType.objects.filter(id=7).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    cogs_credit = AccountType.objects.filter(id=7).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    oe_debit = AccountType.objects.filter(id=8).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    oe_credit = AccountType.objects.filter(id=8).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    transportaion_debit = AccountType.objects.filter(id=9).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    transportaion_credit = AccountType.objects.filter(id=9).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    charity_debit = AccountType.objects.filter(id=10).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    charity_credit = AccountType.objects.filter(id=10).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    repair_debit = AccountType.objects.filter(id=11).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    repair_credit = AccountType.objects.filter(id=11).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    rental_debit = AccountType.objects.filter(id=12).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    rental_credit = AccountType.objects.filter(id=12).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    govt_debit = AccountType.objects.filter(id=13).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    govt_credit = AccountType.objects.filter(id=13).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    bank_debit = AccountType.objects.filter(id=14).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    bank_credit = AccountType.objects.filter(id=14).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    allowance_debit = AccountType.objects.filter(id=15).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    allowance_credit = AccountType.objects.filter(id=15).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    salary_debit = AccountType.objects.filter(id=16).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    salary_credit = AccountType.objects.filter(id=16).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    miscellaneous_debit = AccountType.objects.filter(id=17).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    miscellaneous_credit = AccountType.objects.filter(id=17).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    utility_debit = AccountType.objects.filter(id=18).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    utility_credit = AccountType.objects.filter(id=18).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))

    return render(request, 'reports/trial_balance.html', context={

        'current_asset_credit': current_asset_credit,
        'current_asset_debit': current_asset_debit,
        'fixed_asset_credit': fixed_asset_credit,
        'fixed_asset_debit': fixed_asset_debit,
        'current_liabilities_debit': current_liabilities_debit,
        'current_liabilities_credit': current_liabilities_credit,
        'capital_debit': capital_debit,
        'capital_credit': capital_credit,
        'sales_revenue_debit': sales_revenue_debit,
        'sales_revenue_credit': sales_revenue_credit,
        'misc_income_debit': misc_income_debit,
        'misc_income_credit': misc_income_credit,
        'cogs_debit': cogs_debit,
        'cogs_credit': cogs_credit,
        'oe_debit': oe_debit,
        'oe_credit': oe_credit,
        'transportaion_debit': transportaion_debit,
        'transportaion_credit': transportaion_credit,
        'charity_debit': charity_debit,
        'charity_credit': charity_credit,
        'repair_debit': repair_debit,
        'repair_credit': repair_credit,
        'rental_debit': rental_debit,
        'rental_credit': rental_credit,
        'govt_debit': govt_debit,
        'govt_credit': govt_credit,
        'bank_debit': bank_debit,
        'bank_credit': bank_credit,
        'allowance_debit': allowance_debit,
        'allowance_credit': allowance_credit,
        'salary_debit': salary_debit,
        'salary_credit': salary_credit,
        'miscellaneous_debit': miscellaneous_debit,
        'miscellaneous_credit': miscellaneous_credit,
        'utility_debit': utility_debit,
        'utility_credit': utility_credit,
    })
