from django.shortcuts import render
from django.db.models import Q
from Accountant.models import ManualJournal, CreateAccount, AccountType, BaseAccount, Transaction

# Create your views here.


def add_product(request):
    # accounts = BaseAccount.objects.filter(Q(base_account__iexact="Income") & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
    #     start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit)))['sum_total']

    accounts = CreateAccount.objects.filter(account_type_id=2)

    # import pdb
    # pdb.set_trace()
    return render(request, 'products/add_product.html', context={'accounts': accounts})
