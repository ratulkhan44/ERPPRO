from django.shortcuts import render
from Accountant.models import ManualJournal, CreateAccount, AccountType, BaseAccount, Transaction
from People.models import *
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q
from datetime import date, datetime
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
    today = date.today()
    fvalue = request.POST
    current_year_first_date = date(today.year, 1, 1)
    current_year_last_date = date(today.year, 12, 31)
    prev_year = today - relativedelta(years=1)
    prev_year_first_day = date(prev_year.year, 1, 1)
    prev_year_last_day = date(prev_year.year, 12, 31)

    def calculateBaseAccountCredit(baseAccount, account, start_date, end_date, transaction_credit, transaction_debit):
        baseAccountTotal = (baseAccount.objects.filter(Q(base_account__iexact=account) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']) or 0
        return baseAccountTotal

    def calculateBaseAccountDebit(baseAccount, account, start_date, end_date, transaction_debit, transaction_credit):
        baseAccountTotal = (baseAccount.objects.filter(Q(base_account__iexact=account) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
        return baseAccountTotal

    def calculateAccountTypeDebit(accountType, account, start_date, end_date, transaction_debit, transaction_credit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
        return accountTypeTotal

    def calculateAccountTypeCredit(accountType, account, start_date, end_date, transaction_credit, transaction_debit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']) or 0
        return accountTypeTotal

    def CalculateAccount(ledger, id, start_date, end_date, transaction_debit, transaction_credit):
        account_total = ledger.objects.filter(Q(account_type_id=id) & Q(transaction_account__date__range=[
            start_date, end_date])).annotate(sum_total=(Coalesce(Sum('transaction_account__'+transaction_debit), 0))-(Coalesce(Sum('transaction_account__'+transaction_credit), 0)))
        return account_total

    current_asset_total = calculateAccountTypeDebit(
        AccountType, 'Current Asset', '1991-01-01', today, 'total_debit', 'total_credit')
    fixed_asset_total = calculateAccountTypeDebit(
        AccountType, 'Fixed Asset', '1991-01-01', today, 'total_debit', 'total_credit')

    current_asset_accounts = CalculateAccount(
        CreateAccount, 2, '1991-01-01', today, 'total_debit', 'total_credit')
    fixed_asset_accounts = CalculateAccount(
        CreateAccount, 1, '1991-01-01', today, 'total_debit', 'total_credit')

    current_liabilities_total = calculateAccountTypeCredit(
        AccountType, 'Current Liabilities', '1991-01-01', today, 'total_credit', 'total_debit')

    liabilities_accounts = CalculateAccount(
        CreateAccount, 3, '1991-01-01', today, 'total_credit', 'total_debit')

    capitals_total = calculateAccountTypeCredit(
        AccountType, 'Capital', '1991-01-01', today, 'total_credit', 'total_debit')

    capitals_accounts = CalculateAccount(
        CreateAccount, 4, '1991-01-01', today, 'total_credit', 'total_debit')

    current_income_total = calculateBaseAccountCredit(
        BaseAccount, 'Income', current_year_first_date, current_year_last_date, 'total_credit', 'total_debit')
    current_expense_total = calculateBaseAccountDebit(
        BaseAccount, 'Expenses', current_year_first_date, current_year_last_date, 'total_debit', 'total_credit')
    current_year_earnings = current_income_total-current_expense_total
    retained_income_total = calculateBaseAccountCredit(
        BaseAccount, 'Income', '1991-01-01', prev_year_last_day, 'total_credit', 'total_debit')
    retained_expense_total = calculateBaseAccountDebit(
        BaseAccount, 'Expenses', '1991-01-01', prev_year_last_day, 'total_debit', 'total_credit')
    retained_earnings = retained_income_total - retained_expense_total
    income_total = calculateBaseAccountCredit(
        BaseAccount, 'Income', '1991-01-01', today, 'total_credit', 'total_debit')
    expense_total = calculateBaseAccountDebit(
        BaseAccount, 'Expenses', '1991-01-01', today, 'total_debit', 'total_credit')
    equity_total = calculateBaseAccountCredit(
        BaseAccount, 'Equity', '1991-01-01', today, 'total_credit', 'total_debit')
    actual_equity = (income_total-expense_total) + equity_total

    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        convert_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        convert_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        current_year_first_date = date(convert_end_date.year, 1, 1)
        current_year_last_date = date(convert_end_date.year, 12, 31)
        prev_year = convert_end_date - relativedelta(years=1)
        prev_year_first_day = date(prev_year.year, 1, 1)
        prev_year_last_day = date(prev_year.year, 12, 31)
        fvalue = request.POST

        current_asset_total = calculateAccountTypeDebit(
            AccountType, 'Current Asset', '1991-01-01', end_date, 'total_debit', 'total_credit')
        fixed_asset_total = calculateAccountTypeDebit(
            AccountType, 'Fixed Asset', '1991-01-01', end_date, 'total_debit', 'total_credit')

        current_asset_accounts = CalculateAccount(
            CreateAccount, 2, '1991-01-01', end_date, 'total_debit', 'total_credit')
        fixed_asset_accounts = CalculateAccount(
            CreateAccount, 1, '1991-01-01', end_date, 'total_debit', 'total_credit')

        current_liabilities_total = calculateAccountTypeCredit(
            AccountType, 'Current Liabilities', '1991-01-01', end_date, 'total_credit', 'total_debit')

        liabilities_accounts = CalculateAccount(
            CreateAccount, 3, '1991-01-01', end_date, 'total_debit', 'total_credit')

        capitals_total = calculateAccountTypeCredit(
            AccountType, 'Capital', '1991-01-01', end_date, 'total_credit', 'total_debit')

        capitals_accounts = CalculateAccount(
            CreateAccount, 4, '1991-01-01', end_date, 'total_credit', 'total_debit')

        current_income_total = calculateBaseAccountCredit(
            BaseAccount, 'Income', current_year_first_date, current_year_last_date, 'total_credit', 'total_debit')
        current_expense_total = calculateBaseAccountDebit(
            BaseAccount, 'Expenses', current_year_first_date, current_year_last_date, 'total_debit', 'total_credit')
        current_year_earnings = current_income_total-current_expense_total
        retained_income_total = calculateBaseAccountCredit(
            BaseAccount, 'Income', '1991-01-01', prev_year_last_day, 'total_credit', 'total_debit')
        retained_expense_total = calculateBaseAccountDebit(
            BaseAccount, 'Expenses', '1991-01-01', prev_year_last_day, 'total_debit', 'total_credit')
        retained_earnings = retained_income_total - retained_expense_total
        income_total = calculateBaseAccountCredit(
            BaseAccount, 'Income', '1991-01-01', end_date, 'total_credit', 'total_debit')
        expense_total = calculateBaseAccountDebit(
            BaseAccount, 'Expenses', '1991-01-01', end_date, 'total_debit', 'total_credit')
        equity_total = calculateBaseAccountCredit(
            BaseAccount, 'Equity', '1991-01-01', end_date, 'total_credit', 'total_debit')
        actual_equity = (income_total-expense_total) + equity_total

        return render(request, 'reports/balance_sheet.html', context={'fvalue': fvalue, 'fixed_asset_accounts': fixed_asset_accounts, 'current_asset_accounts': current_asset_accounts, 'current_asset_total': current_asset_total, 'fixed_asset_total': fixed_asset_total, 'current_liabilities_total': current_liabilities_total, 'liabilities_accounts': liabilities_accounts, 'capitals_accounts': capitals_accounts, 'current_year_earnings': current_year_earnings, 'retained_earnings': retained_earnings, 'actual_equity': actual_equity})

    return render(request, 'reports/balance_sheet.html', context={'fvalue': fvalue, 'fixed_asset_accounts': fixed_asset_accounts, 'current_asset_accounts': current_asset_accounts, 'current_asset_total': current_asset_total, 'fixed_asset_total': fixed_asset_total, 'current_liabilities_total': current_liabilities_total, 'liabilities_accounts': liabilities_accounts, 'capitals_total': capitals_total, 'capitals_accounts': capitals_accounts, 'current_year_earnings': current_year_earnings, 'retained_earnings': retained_earnings, 'actual_equity': actual_equity, 'today': today})


def trial_balance(request):
    today = date.today()

    def calculateAccountTypeDebit(accountType, account, start_date, end_date, transaction_debit, transaction_credit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
        return accountTypeTotal

    def calculateAccountTypeCredit(accountType, account, start_date, end_date, transaction_credit, transaction_debit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']) or 0
        return accountTypeTotal

    def calculateAccountCredit(ledger, id, start_date, end_date, transaction_credit, transaction_debit):
        account_total = ledger.objects.filter(Q(account_type_id=id) & Q(transaction_account__date__range=[
            start_date, end_date])).annotate(sum_total=(Coalesce(Sum('transaction_account__'+transaction_credit), 0))-(Coalesce(Sum('transaction_account__'+transaction_debit), 0)))
        return account_total

    def calculateAccountDebit(ledger, id, start_date, end_date, transaction_debit, transaction_credit):
        account_total = ledger.objects.filter(Q(account_type_id=id) & Q(transaction_account__date__range=[
            start_date, end_date])).annotate(sum_total=(Coalesce(Sum('transaction_account__'+transaction_debit), 0))-(Coalesce(Sum('transaction_account__'+transaction_credit), 0)))
        return account_total

    a = Transaction.objects.filter()

    current_asset_total = calculateAccountTypeDebit(
        AccountType, 'Current Asset', '1991-01-01', today, 'total_debit', 'total_credit')

    current_asset_ledger = calculateAccountDebit(
        CreateAccount, 2, '1991-01-01', today, 'total_debit', 'total_credit')

    fixed_asset_total = calculateAccountTypeDebit(
        AccountType, 'Fixed Asset', '1991-01-01', today, 'total_debit', 'total_credit')

    fixed_asset_ledger = calculateAccountCredit(
        CreateAccount, 1, '1991-01-01', today, 'total_debit', 'total_credit')

    capital_total = calculateAccountTypeCredit(
        AccountType, 'Capital', '1991-01-01', today, 'total_credit', 'total_debit')

    capital_ledger = calculateAccountCredit(
        CreateAccount, 4, '1991-01-01', today, 'total_credit', 'total_debit')

    sales_total = calculateAccountTypeCredit(
        AccountType, 'Sales Revenue', '1991-01-01', today, 'total_credit', 'total_debit')

    sales_ledger = calculateAccountCredit(
        CreateAccount, 5, '1991-01-01', today, 'total_credit', 'total_debit')

    misc_total = calculateAccountTypeCredit(
        AccountType, 'Misc. Income', '1991-01-01', today, 'total_credit', 'total_debit')

    misc_ledger = calculateAccountCredit(
        CreateAccount, 6, '1991-01-01', today, 'total_credit', 'total_debit')

    cogs_total = calculateAccountTypeDebit(
        AccountType, 'COGS', '1991-01-01', today, 'total_debit', 'total_credit')

    cogs_ledger = calculateAccountDebit(
        CreateAccount, 7, '1991-01-01', today, 'total_debit', 'total_credit')

    oe_total = calculateAccountTypeDebit(
        AccountType, 'Operating Expenses', '1991-01-01', today, 'total_debit', 'total_credit')

    oe_ledger = calculateAccountDebit(
        CreateAccount, 8, '1991-01-01', today, 'total_debit', 'total_credit')

    transportation_total = calculateAccountTypeDebit(
        AccountType, 'Transporation', '1991-01-01', today, 'total_debit', 'total_credit')

    transportaion_ledger = calculateAccountDebit(
        CreateAccount, 9, '1991-01-01', today, 'total_debit', 'total_credit')

    charity_total = calculateAccountTypeDebit(
        AccountType, 'Charity & Donation', '1991-01-01', today, 'total_debit', 'total_credit')

    charity_ledger = calculateAccountDebit(
        CreateAccount, 10, '1991-01-01', today, 'total_debit', 'total_credit')

    repair_total = calculateAccountTypeDebit(
        AccountType, 'Repair & Maintenance', '1991-01-01', today, 'total_debit', 'total_credit')

    repair_ledger = calculateAccountDebit(
        CreateAccount, 11, '1991-01-01', today, 'total_debit', 'total_credit')

    rental_total = calculateAccountTypeDebit(
        AccountType, 'Rental Expenses', '1991-01-01', today, 'total_debit', 'total_credit')

    rental_ledger = calculateAccountDebit(
        CreateAccount, 12, '1991-01-01', today, 'total_debit', 'total_credit')

    govt_total = calculateAccountTypeDebit(
        AccountType, 'Government & Legal Fee', '1991-01-01', today, 'total_debit', 'total_credit')

    govt_ledger = calculateAccountDebit(
        CreateAccount, 13, '1991-01-01', today, 'total_debit', 'total_credit')

    bank_total = calculateAccountTypeDebit(
        AccountType, 'Banking Expenses', '1991-01-01', today, 'total_debit', 'total_credit')

    bank_ledger = calculateAccountDebit(
        CreateAccount, 14, '1991-01-01', today, 'total_debit', 'total_credit')

    allowance_total = calculateAccountTypeDebit(
        AccountType, 'Allowance', '1991-01-01', today, 'total_debit', 'total_credit')

    allowance_ledger = calculateAccountDebit(
        CreateAccount, 15, '1991-01-01', today, 'total_debit', 'total_credit')

    salary_total = calculateAccountTypeDebit(
        AccountType, 'Salary', '1991-01-01', today, 'total_debit', 'total_credit')

    salary_ledger = calculateAccountDebit(
        CreateAccount, 16, '1991-01-01', today, 'total_debit', 'total_credit')

    miscellanous_total = calculateAccountTypeDebit(
        AccountType, 'Miscellaneous Expense', '1991-01-01', today, 'total_debit', 'total_credit')

    miscellanous_ledger = calculateAccountDebit(
        CreateAccount, 17, '1991-01-01', today, 'total_debit', 'total_credit')

    utility_total = calculateAccountTypeDebit(
        AccountType, 'Utility Expenses', '1991-01-01', today, 'total_debit', 'total_credit')

    utility_ledger = calculateAccountDebit(
        CreateAccount, 18, '1991-01-01', today, 'total_debit', 'total_credit')

    asset_total = current_asset_total+fixed_asset_total
    equity_total = capital_total
    income_total = sales_total+misc_total
    expense_total = oe_total+cogs_total+transportation_total+charity_total+repair_total + \
        rental_total+govt_total+bank_total+allowance_total + \
        salary_total+miscellanous_total+utility_total

    return render(request, 'reports/trial_balance.html', context={
        'current_asset_total': current_asset_total,
        'current_asset_ledger': current_asset_ledger,
        'fixed_asset_total': fixed_asset_total,
        'fixed_asset_ledger': fixed_asset_ledger,
        'capital_total': capital_total,
        'capital_ledger': capital_ledger,
        'sales_total': sales_total,
        'sales_ledger': sales_ledger,
        'misc_total': misc_total,
        'misc_ledger': misc_ledger,
        'cogs_total': cogs_total,
        'cogs_ledger': cogs_ledger,
        'oe_total': oe_total,
        'oe_ledger': oe_ledger,
        'transportation_total': transportation_total,
        'transportaion_ledger': transportaion_ledger,
        'charity_total': charity_total,
        'charity_ledger': charity_ledger,
        'repair_total': repair_total,
        'repair_ledger': repair_ledger,
        'rental_total': rental_total,
        'rental_ledger': rental_ledger,
        'govt_total': govt_total,
        'govt_ledger': govt_ledger,
        'bank_total': bank_total,
        'bank_ledger': bank_ledger,
        'allowance_total': allowance_total,
        'allowance_ledger': allowance_ledger,
        'salary_total': salary_total,
        'salary_ledger': salary_ledger,
        'miscellanous_total': miscellanous_total,
        'miscellanous_ledger': miscellanous_ledger,
        'utility_total': utility_total,
        'utility_ledger': utility_ledger,
    })


def profit_loss(request):
    today = date.today()
    fvalue = request.POST
    start_date = date(today.year, 1, 1)
    end_date = date(today.year, 12, 31)

    def calculateAccountTypeDebit(accountType, account, start_date, end_date, transaction_debit, transaction_credit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
        return accountTypeTotal

    def calculateAccountTypecredit(accountType, account, start_date, end_date, transaction_credit, transaction_debit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']) or 0
        return accountTypeTotal

    sales_total = calculateAccountTypecredit(
        AccountType, 'Sales Revenue', start_date, end_date, 'total_credit', 'total_debit')

    misc_income_total = calculateAccountTypecredit(
        AccountType, 'Misc. Income', start_date, end_date, 'total_credit', 'total_debit')
    income_total = sales_total+misc_income_total

    cogs_total = calculateAccountTypeDebit(
        AccountType, 'cogs', start_date, end_date, 'total_debit', 'total_credit')

    gross_profit = income_total-cogs_total

    oe_total = calculateAccountTypeDebit(
        AccountType, 'Operating Expenses', start_date, end_date, 'total_debit', 'total_credit')

    transportaion_total = calculateAccountTypeDebit(
        AccountType, 'Transporation', start_date, end_date, 'total_debit', 'total_credit')
    charity_total = calculateAccountTypeDebit(
        AccountType, 'Charity & Donation', start_date, end_date, 'total_debit', 'total_credit')

    repair_total = calculateAccountTypeDebit(
        AccountType, 'Repair & Maintenance', start_date, end_date, 'total_debit', 'total_credit')

    rental_total = calculateAccountTypeDebit(
        AccountType, 'Rental Expenses', start_date, end_date, 'total_debit', 'total_credit')

    govt_total = calculateAccountTypeDebit(
        AccountType, 'Government & Legal Fee', start_date, end_date, 'total_debit', 'total_credit')

    bank_total = calculateAccountTypeDebit(
        AccountType, 'Banking Expenses', start_date, end_date, 'total_debit', 'total_credit')

    allowance_total = calculateAccountTypeDebit(
        AccountType, 'Allowance', start_date, end_date, 'total_debit', 'total_credit')

    salary_total = calculateAccountTypeDebit(
        AccountType, 'Salary', start_date, end_date, 'total_debit', 'total_credit')

    miscellaneous_total = calculateAccountTypeDebit(
        AccountType, 'Miscellaneous Expense', start_date, end_date, 'total_debit', 'total_credit')

    utility_total = calculateAccountTypeDebit(
        AccountType, 'Utility Expenses', start_date, end_date, 'total_debit', 'total_credit')

    all_expenses = oe_total + transportaion_total + charity_total+repair_total + rental_total + \
        govt_total+bank_total + allowance_total + \
        salary_total + miscellaneous_total + utility_total

    net_profit = gross_profit - all_expenses

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        sales_total = calculateAccountTypecredit(
            AccountType, 'Sales Revenue', start_date, end_date, 'total_credit', 'total_debit')

        misc_income_total = calculateAccountTypecredit(
            AccountType, 'Misc. Income', start_date, end_date, 'total_credit', 'total_debit')
        income_total = sales_total+misc_income_total

        cogs_total = calculateAccountTypeDebit(
            AccountType, 'cogs', start_date, end_date, 'total_debit', 'total_credit')

        gross_profit = income_total-cogs_total

        oe_total = calculateAccountTypeDebit(
            AccountType, 'Operating Expenses', start_date, end_date, 'total_debit', 'total_credit')

        transportaion_total = calculateAccountTypeDebit(
            AccountType, 'Transporation', start_date, end_date, 'total_debit', 'total_credit')
        charity_total = calculateAccountTypeDebit(
            AccountType, 'Charity & Donation', start_date, end_date, 'total_debit', 'total_credit')

        repair_total = calculateAccountTypeDebit(
            AccountType, 'Repair & Maintenance', start_date, end_date, 'total_debit', 'total_credit')

        rental_total = calculateAccountTypeDebit(
            AccountType, 'Rental Expenses', start_date, end_date, 'total_debit', 'total_credit')

        govt_total = calculateAccountTypeDebit(
            AccountType, 'Government & Legal Fee', start_date, end_date, 'total_debit', 'total_credit')

        bank_total = calculateAccountTypeDebit(
            AccountType, 'Banking Expenses', start_date, end_date, 'total_debit', 'total_credit')

        allowance_total = calculateAccountTypeDebit(
            AccountType, 'Allowance', start_date, end_date, 'total_debit', 'total_credit')

        salary_total = calculateAccountTypeDebit(
            AccountType, 'Salary', start_date, end_date, 'total_debit', 'total_credit')

        miscellaneous_total = calculateAccountTypeDebit(
            AccountType, 'Miscellaneous Expense', start_date, end_date, 'total_debit', 'total_credit')

        utility_total = calculateAccountTypeDebit(
            AccountType, 'Utility Expenses', start_date, end_date, 'total_debit', 'total_credit')

        all_expenses = oe_total + transportaion_total + charity_total+repair_total + rental_total + \
            govt_total+bank_total + allowance_total + \
            salary_total + miscellaneous_total + utility_total

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
            'start_date': start_date,
            'end_date': end_date
        })

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
        'start_date': start_date,
        'end_date': end_date
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
    current_year_first_date = date(today.year, 1, 1)
    current_year_last_date = date(today.year, 12, 31)
    prev_year = today - relativedelta(years=1)
    prev_year_first_day = date(prev_year.year, 1, 1)
    prev_year_last_day = date(prev_year.year, 12, 31)

    def calculateBaseAccountCredit(baseAccount, account, start_date, end_date, transaction_credit, transaction_debit):
        baseAccountTotal = (baseAccount.objects.filter(Q(base_account__iexact=account) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']) or 0
        return baseAccountTotal

    def calculateBaseAccountDebit(baseAccount, account, start_date, end_date, transaction_debit, transaction_credit):
        baseAccountTotal = (baseAccount.objects.filter(Q(base_account__iexact=account) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
        return baseAccountTotal

    def calculateAccountTypeDebit(accountType, account, start_date, end_date, transaction_debit, transaction_credit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
        return accountTypeTotal

    def calculateAccountTypeCredit(accountType, account, start_date, end_date, transaction_credit, transaction_debit):
        accountTypeTotal = (accountType.objects.filter(Q(account_type__iexact=account) & Q(createaccount_account_type__transaction_account__date__range=[
            start_date, end_date])).aggregate(sum_total=(Sum('createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']) or 0
        return accountTypeTotal

    def CalculateAccount(ledger, id, start_date, end_date, transaction_debit, transaction_credit):
        account_total = ledger.objects.filter(Q(account_type_id=id) & Q(transaction_account__date__range=[
            start_date, end_date])).annotate(sum_total=(Coalesce(Sum('transaction_account__'+transaction_debit), 0))-(Coalesce(Sum('transaction_account__'+transaction_credit), 0)))
        return account_total

    current_asset_total = calculateAccountTypeDebit(
        AccountType, 'Current Asset', '1991-01-01', today, 'total_debit', 'total_credit')
    fixed_asset_total = calculateAccountTypeDebit(
        AccountType, 'Fixed Asset', '1991-01-01', today, 'total_debit', 'total_credit')

    current_asset_accounts = CalculateAccount(
        CreateAccount, 2, '1991-01-01', today, 'total_debit', 'total_credit')
    fixed_asset_accounts = CalculateAccount(
        CreateAccount, 1, '1991-01-01', today, 'total_debit', 'total_credit')

    current_liabilities_total = calculateAccountTypeCredit(
        AccountType, 'Current Liabilities', '1991-01-01', today, 'total_credit', 'total_debit')

    liabilities_accounts = CalculateAccount(
        CreateAccount, 3, '1991-01-01', today, 'total_credit', 'total_debit')

    capitals_total = calculateAccountTypeCredit(
        AccountType, 'Capital', '1991-01-01', today, 'total_credit', 'total_debit')

    capitals_accounts = CalculateAccount(
        CreateAccount, 4, '1991-01-01', today, 'total_credit', 'total_debit')

    current_income_total = calculateBaseAccountCredit(
        BaseAccount, 'Income', current_year_first_date, current_year_last_date, 'total_credit', 'total_debit')
    current_expense_total = calculateBaseAccountDebit(
        BaseAccount, 'Expenses', current_year_first_date, current_year_last_date, 'total_debit', 'total_credit')
    current_year_earnings = current_income_total-current_expense_total
    retained_income_total = calculateBaseAccountCredit(
        BaseAccount, 'Income', '1991-01-01', prev_year_last_day, 'total_credit', 'total_debit')
    retained_expense_total = calculateBaseAccountDebit(
        BaseAccount, 'Expenses', '1991-01-01', prev_year_last_day, 'total_debit', 'total_credit')
    retained_earnings = retained_income_total - retained_expense_total
    income_total = calculateBaseAccountCredit(
        BaseAccount, 'Income', '1991-01-01', today, 'total_credit', 'total_debit')
    expense_total = calculateBaseAccountDebit(
        BaseAccount, 'Expenses', '1991-01-01', today, 'total_debit', 'total_credit')
    equity_total = calculateBaseAccountCredit(
        BaseAccount, 'Equity', '1991-01-01', today, 'total_credit', 'total_debit')
    actual_equity = (income_total-expense_total) + equity_total

    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        convert_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        convert_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        current_year_first_date = date(convert_end_date.year, 1, 1)
        current_year_last_date = date(convert_end_date.year, 12, 31)
        prev_year = convert_end_date - relativedelta(years=1)
        prev_year_first_day = date(prev_year.year, 1, 1)
        prev_year_last_day = date(prev_year.year, 12, 31)
        fvalue = request.POST

        current_asset_total = calculateAccountTypeDebit(
            AccountType, 'Current Asset', '1991-01-01', end_date, 'total_debit', 'total_credit')
        fixed_asset_total = calculateAccountTypeDebit(
            AccountType, 'Fixed Asset', '1991-01-01', end_date, 'total_debit', 'total_credit')

        current_asset_accounts = CalculateAccount(
            CreateAccount, 2, '1991-01-01', end_date, 'total_debit', 'total_credit')
        fixed_asset_accounts = CalculateAccount(
            CreateAccount, 1, '1991-01-01', end_date, 'total_debit', 'total_credit')

        current_liabilities_total = calculateAccountTypeCredit(
            AccountType, 'Current Liabilities', '1991-01-01', end_date, 'total_credit', 'total_debit')

        liabilities_accounts = CalculateAccount(
            CreateAccount, 3, '1991-01-01', end_date, 'total_debit', 'total_credit')

        capitals_total = calculateAccountTypeCredit(
            AccountType, 'Capital', '1991-01-01', end_date, 'total_credit', 'total_debit')

        capitals_accounts = CalculateAccount(
            CreateAccount, 4, '1991-01-01', end_date, 'total_credit', 'total_debit')

        current_income_total = calculateBaseAccountCredit(
            BaseAccount, 'Income', current_year_first_date, current_year_last_date, 'total_credit', 'total_debit')
        current_expense_total = calculateBaseAccountDebit(
            BaseAccount, 'Expenses', current_year_first_date, current_year_last_date, 'total_debit', 'total_credit')
        current_year_earnings = current_income_total-current_expense_total
        retained_income_total = calculateBaseAccountCredit(
            BaseAccount, 'Income', '1991-01-01', prev_year_last_day, 'total_credit', 'total_debit')
        retained_expense_total = calculateBaseAccountDebit(
            BaseAccount, 'Expenses', '1991-01-01', prev_year_last_day, 'total_debit', 'total_credit')
        retained_earnings = retained_income_total - retained_expense_total
        income_total = calculateBaseAccountCredit(
            BaseAccount, 'Income', '1991-01-01', end_date, 'total_credit', 'total_debit')
        expense_total = calculateBaseAccountDebit(
            BaseAccount, 'Expenses', '1991-01-01', end_date, 'total_debit', 'total_credit')
        equity_total = calculateBaseAccountCredit(
            BaseAccount, 'Equity', '1991-01-01', end_date, 'total_credit', 'total_debit')
        actual_equity = (income_total-expense_total) + equity_total

        return render(request, 'reports/date_filter.html', context={'fvalue': fvalue, 'fixed_asset_accounts': fixed_asset_accounts, 'current_asset_accounts': current_asset_accounts, 'current_asset_total': current_asset_total, 'fixed_asset_total': fixed_asset_total, 'current_liabilities_total': current_liabilities_total, 'liabilities_accounts': liabilities_accounts, 'capitals_accounts': capitals_accounts, 'current_year_earnings': current_year_earnings, 'retained_earnings': retained_earnings, 'actual_equity': actual_equity})

    return render(request, 'reports/date_filter.html', context={'fvalue': fvalue, 'fixed_asset_accounts': fixed_asset_accounts, 'current_asset_accounts': current_asset_accounts, 'current_asset_total': current_asset_total, 'fixed_asset_total': fixed_asset_total, 'current_liabilities_total': current_liabilities_total, 'liabilities_accounts': liabilities_accounts, 'capitals_total': capitals_total, 'capitals_accounts': capitals_accounts, 'current_year_earnings': current_year_earnings, 'retained_earnings': retained_earnings, 'actual_equity': actual_equity})
