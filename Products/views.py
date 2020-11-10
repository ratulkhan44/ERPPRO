from django.shortcuts import render
from django.db.models import Q
from Accountant.models import ManualJournal, CreateAccount, AccountType, BaseAccount, Transaction

# Create your views here.


def add_product(request):
    # accounts = BaseAccount.objects.filter(Q(base_account__iexact="Income") & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
    #     start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']

    sales_accounts = CreateAccount.objects.filter(
        Q(account_type_id=5) | Q(account_type_id=6))
    purchase_accounts = CreateAccount.objects.filter(account_type_id=7)
    inventory_account = CreateAccount.objects.get(
        account_name__iexact='inventory')

    # import pdb
    # pdb.set_trace()
    return render(request, 'products/add_product.html', context={'sales_accounts': sales_accounts, 'purchase_accounts': purchase_accounts, 'inventory_account': inventory_account})
