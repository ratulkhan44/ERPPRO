from django.shortcuts import render, HttpResponseRedirect
from Accountant.models import *
from Accountant import forms
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
import json
import decimal
# Create your views here.


def chart_of_account(request):
    return render(request, 'accountant/chart_of_account.html', context={})


def base_account(request):
    form = forms.BaseAccountForm()

    if request.method == 'POST':
        form = forms.BaseAccountForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Base Account Created Successfully')
            return HttpResponseRedirect(reverse('Accountant:base_account'))

    return render(request, 'accountant/base_account.html', context={'form': form})


def account_type(request):
    form = forms.AccountTypeForm()
    if request.method == 'POST':
        form = forms.AccountTypeForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Account Type Created Successfully')
            return HttpResponseRedirect(reverse('Accountant:account_type'))

    account_types = AccountType.objects.all()
    return render(request, 'accountant/account_type.html', context={'form': form, 'account_types': account_types})


def manual_journal(request):

    accounts = CreateAccount.objects.all()
    peoples = People.objects.all()
    if request.method == "POST":
        data = json.loads(request.body)
        voucher_date = data['voucher_date']
        voucher_no = data['voucher_no']
        reference = data['reference']
        notes = data['notes']
        account = data['account']
        particular = data['particular']
        people_for_from = data['people_for_from']
        people_by = data['people_by']
        debit = data['debit']
        credit = data['credit']

        account_id = CreateAccount.objects.get(id=account)
        total_debit = account_id.total_debit+decimal.Decimal(debit)
        total_credit = account_id.total_credit+decimal.Decimal(credit)
        CreateAccount.objects.filter(
            id=account).update(total_debit=total_debit, total_credit=total_credit)

        ManualJournal.objects.create(voucher_date=voucher_date, voucher_no=voucher_no, reference=reference, notes=notes, account_id=account,
                                     particular=particular, people_for_from_id=people_for_from, people_by_id=people_by, debit=debit, credit=credit)
        messages.success(request, 'Journal Created Successfully')

    return render(request, 'accountant/manual_journal.html', context={'accounts': accounts, 'peoples': peoples})


def all_journal(request):
    journals = ManualJournal.objects.all()

    return render(request, 'accountant/alljournal.html', context={'journals': journals})


# def create_account(request):
#     form = forms.AccountForm()

#     if request.method == 'POST':

#         form = forms.AccountForm(request.POST)

#         if form.is_valid():
#             form.save(commit=True)
#             messages.success(request, 'Account Created Successfully')
#             return HttpResponseRedirect(reverse('Accountant:create_account'))

#         # account_type = request.POST.get('account_type')
#         # account_name = request.POST.get('account_name')
#         # account_code = request.POST.get('account_code')
#         # description = request.POST.get('description')

#         # CreateAccount.objects.create(account_type=account_type, account_name=account_name,
#         #                              account_code=account_code, description=description)

#     return render(request, 'accountant/create_account.html', context={'form': form})


def chart_of_accounts(request):
    form = forms.AccountForm()

    if request.method == 'POST':

        form = forms.AccountForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Account Created Successfully')

    accounts = CreateAccount.objects.all()
    return render(request, 'accountant/chart_of_account.html', context={'form': form, 'accounts': accounts})


def demo_journal(request):
    pass
