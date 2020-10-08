from django.shortcuts import render
from Accountant.models import ManualJournal, CreateAccount, AccountType, BaseAccount, Transaction
from People.models import *
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models.functions import Coalesce

# Create your views here.


def allreports(request):
    return render(request, 'reports/allreports.html', context={})


def general_ledger(request):
    accounts = CreateAccount.objects.all().order_by('account_name')

    # journal_accounts = ManualJournal.objects.all()
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
    # asset_debit = BaseAccount.objects.filter(id=2).aggregate(
    # sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    # print(a)
    # abc = a.createaccount_account_type.all()
    return render(request, 'reports/account_transactions.html', context={'accounts': accounts, 'account_name': account_name})


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
    today = date.today()
    current_asset_credit = BaseAccount.objects.filter(Q(id=2) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    current_asset_debit = BaseAccount.objects.filter(Q(id=2) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    fixed_asset_credit = BaseAccount.objects.filter(Q(id=1) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    fixed_asset_debit = BaseAccount.objects.filter(Q(id=1) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    current_liabilities_debit = BaseAccount.objects.filter(Q(id=3) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    current_liabilities_credit = BaseAccount.objects.filter(Q(id=3) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    capital_debit = BaseAccount.objects.filter(Q(id=4) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    capital_credit = BaseAccount.objects.filter(Q(id=4) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    sales_revenue_debit = BaseAccount.objects.filter(Q(id=5) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    sales_revenue_credit = BaseAccount.objects.filter(Q(id=5) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    misc_income_debit = BaseAccount.objects.filter(Q(id=6) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    misc_income_credit = BaseAccount.objects.filter(Q(id=6) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    cogs_debit = BaseAccount.objects.filter(Q(id=7) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    cogs_credit = BaseAccount.objects.filter(Q(id=7) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    oe_debit = BaseAccount.objects.filter(Q(id=8) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    oe_credit = BaseAccount.objects.filter(Q(id=8) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    transportaion_debit = BaseAccount.objects.filter(Q(id=9) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    transportaion_credit = BaseAccount.objects.filter(Q(id=9) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    charity_debit = BaseAccount.objects.filter(Q(id=10) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    charity_credit = BaseAccount.objects.filter(Q(id=10) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    repair_debit = BaseAccount.objects.filter(Q(id=11) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    repair_credit = BaseAccount.objects.filter(Q(id=11) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    rental_debit = BaseAccount.objects.filter(Q(id=12) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    rental_credit = BaseAccount.objects.filter(Q(id=12) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    govt_debit = BaseAccount.objects.filter(Q(id=13) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    govt_credit = BaseAccount.objects.filter(Q(id=13) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    bank_debit = BaseAccount.objects.filter(Q(id=14) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    bank_credit = BaseAccount.objects.filter(Q(id=14) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    allowance_debit = BaseAccount.objects.filter(Q(id=15) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    allowance_credit = BaseAccount.objects.filter(Q(id=15) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    salary_debit = BaseAccount.objects.filter(Q(id=16) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    salary_credit = BaseAccount.objects.filter(Q(id=16) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    miscellaneous_debit = BaseAccount.objects.filter(Q(id=17) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    miscellaneous_credit = BaseAccount.objects.filter(Q(id=17) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

    utility_debit = BaseAccount.objects.filter(Q(id=18) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_debit'))

    utility_credit = BaseAccount.objects.filter(Q(id=18) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
        today, today])).aggregate(sum_total=Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__total_credit'))

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


def profit_loss(request):
    sales_revenue_debit = AccountType.objects.filter(id=5).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))

    sales_revenue_credit = AccountType.objects.filter(id=5).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    sales_total = sales_revenue_credit['sum_total'] - \
        sales_revenue_debit['sum_total']
    print(sales_total)
    misc_income_debit = AccountType.objects.filter(id=6).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    misc_income_credit = AccountType.objects.filter(id=6).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    misc_income_total = misc_income_credit['sum_total'] - \
        misc_income_debit['sum_total']
    income_total = sales_total+misc_income_total

    cogs_debit = AccountType.objects.filter(id=7).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    cogs_credit = AccountType.objects.filter(id=7).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    cogs_total = cogs_debit['sum_total'] - cogs_credit['sum_total']

    gross_profit = income_total-cogs_total
    print(gross_profit)

    oe_debit = AccountType.objects.filter(id=8).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    oe_credit = AccountType.objects.filter(id=8).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    oe_total = oe_debit['sum_total'] - oe_credit['sum_total']

    transportaion_debit = AccountType.objects.filter(id=9).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    transportaion_credit = AccountType.objects.filter(id=9).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    transportaion_total = transportaion_debit['sum_total'] - \
        transportaion_credit['sum_total']

    charity_debit = AccountType.objects.filter(id=10).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    charity_credit = AccountType.objects.filter(id=10).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    charity_total = charity_debit['sum_total']-charity_credit['sum_total']

    repair_debit = AccountType.objects.filter(id=11).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    repair_credit = AccountType.objects.filter(id=11).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    repair_total = repair_debit['sum_total'] - repair_credit['sum_total']

    rental_debit = AccountType.objects.filter(id=12).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    rental_credit = AccountType.objects.filter(id=12).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    rental_total = rental_debit['sum_total'] - rental_credit['sum_total']

    govt_debit = AccountType.objects.filter(id=13).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    govt_credit = AccountType.objects.filter(id=13).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    govt_total = govt_debit['sum_total']-govt_credit['sum_total']

    bank_debit = AccountType.objects.filter(id=14).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    bank_credit = AccountType.objects.filter(id=14).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    bank_total = bank_debit['sum_total']-bank_credit['sum_total']

    allowance_debit = AccountType.objects.filter(id=15).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    allowance_credit = AccountType.objects.filter(id=15).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    allowance_total = allowance_debit['sum_total'] - \
        allowance_credit['sum_total']

    salary_debit = AccountType.objects.filter(id=16).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    salary_credit = AccountType.objects.filter(id=16).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    salary_total = salary_debit['sum_total']-salary_credit['sum_total']

    miscellaneous_debit = AccountType.objects.filter(id=17).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    miscellaneous_credit = AccountType.objects.filter(id=17).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    miscellaneous_total = miscellaneous_debit['sum_total'] - \
        miscellaneous_credit['sum_total']

    utility_debit = AccountType.objects.filter(id=18).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    utility_credit = AccountType.objects.filter(id=18).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    utility_total = utility_debit['sum_total']-utility_credit['sum_total']

    all_expenses = oe_total + transportaion_total + charity_total+repair_total + rental_total + \
        govt_total+bank_total + allowance_total + \
        salary_total + miscellaneous_total + utility_total
    print(cogs_total)
    print(all_expenses)

    net_profit = gross_profit - all_expenses

    return render(request, 'reports/profit_loss.html', context={
        'sales_total': sales_total,
        'misc_income_total': misc_income_total,
        'income_total': income_total,
        'cogs_total': cogs_total,
        'oe_total': oe_total,
        'transportaion_total': transportaion_total,
        'charity_total': charity_total,
        'repair_total': repair_total,
        'rental_total': rental_total,
        'govt_total': govt_total,
        'bank_total': bank_total,
        'allowance_total': allowance_total,
        'salary_total': salary_total,
        'miscellaneous_total': miscellaneous_total,
        'utility_total': utility_total,
        'all_expenses': all_expenses,
        'net_profit': net_profit,
        'gross_profit': gross_profit,
    })


def demo(request):
    asset_debit = BaseAccount.objects.filter(id=1).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_debit'))
    asset_credit = BaseAccount.objects.filter(id=1).aggregate(
        sum_total=Sum('accounttype_baseaccount__createaccount_account_type__total_credit'))
    asset_total = asset_debit['sum_total']-asset_credit['sum_total']
    current_asset_credit = AccountType.objects.filter(id=2).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    current_asset_debit = AccountType.objects.filter(id=2).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))
    fixed_asset_credit = AccountType.objects.filter(id=1).aggregate(
        sum_total=Sum('createaccount_account_type__total_credit'))
    fixed_asset_debit = AccountType.objects.filter(id=1).aggregate(
        sum_total=Sum('createaccount_account_type__total_debit'))

    current_asset_total = current_asset_debit['sum_total'] - \
        current_asset_credit['sum_total']
    fixed_asset_total = fixed_asset_debit['sum_total'] - \
        fixed_asset_credit['sum_total']

    # account_types = AccountType.objects.filter(base_account=1)
    fixed_assets = CreateAccount.objects.filter(
        Q(account_type=1) & (Q(total_credit__gt=0) | Q(total_debit__gt=0)))
    current_assets = CreateAccount.objects.filter(
        Q(account_type=2) & (Q(total_credit__gt=0) | Q(total_debit__gt=0)))
    # print("blncccc", current_asset_total)
    return render(request, 'reports/demo.html', context={'fixed_assets': fixed_assets, 'current_assets': current_assets, 'current_asset_total': current_asset_total, 'fixed_asset_total': fixed_asset_total})


def date_filter(request):
    today = date.today()

    fvalue = request.POST

    current_assets = CreateAccount.objects.filter(Q(account_type_id=2) & Q(transaction_account__date__range=[
        '1991-01-01', today])).annotate(sum_total=(Coalesce(Sum('transaction_account__total_debit'), 0))-(Coalesce(Sum('transaction_account__total_credit'), 0)))
    fixed_assets = CreateAccount.objects.filter(Q(account_type_id=1) & Q(transaction_account__date__range=[
        '1991-01-01', today])).annotate(sum_total=(Coalesce(Sum('transaction_account__total_debit'), 0))-(Coalesce(Sum('transaction_account__total_credit'), 0)))

    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        current_assets = CreateAccount.objects.filter(Q(account_type_id=2) & Q(transaction_account__date__range=[
            start_date, end_date])).annotate(sum_total=(Coalesce(Sum('transaction_account__total_debit'), 0))-(Coalesce(Sum('transaction_account__total_credit'), 0)))
        fixed_assets = CreateAccount.objects.filter(Q(account_type_id=1) & Q(transaction_account__date__range=[
            start_date, end_date])).annotate(sum_total=(Coalesce(Sum('transaction_account__total_debit'), 0))-(Coalesce(Sum('transaction_account__total_credit'), 0)))

        return render(request, 'reports/date_filter.html', context={'fvalue': fvalue, 'fixed_assets': fixed_assets, 'current_assets': current_assets})
        # diction.update({'current_asset_credit': current_asset_credit})

    return render(request, 'reports/date_filter.html', context={'fvalue': fvalue, 'fixed_assets': fixed_assets, 'current_assets': current_assets})
