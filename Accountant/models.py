from django.db import models
from People.models import *


# Create your models here.


class BaseAccount(models.Model):
    base_account = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.base_account


class AccountType(models.Model):
    base_account = models.ForeignKey(
        BaseAccount, on_delete=models.CASCADE, related_name='accounttype_baseaccount')
    account_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.account_type


class CreateAccount(models.Model):
    account_type = models.ForeignKey(
        AccountType, on_delete=models.CASCADE, related_name='createaccount_account_type')
    account_name = models.CharField(max_length=100, unique=True)
    account_code = models.IntegerField(unique=True)
    description = models.TextField(blank=True, null=True)
    total_debit = models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2)
    total_credit = models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2)

    def __str__(self):
        return self.account_name


class ManualJournal(models.Model):
    voucher_no = models.CharField(max_length=100)
    voucher_date = models.DateField()
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    account = models.ForeignKey(
        CreateAccount, on_delete=models.CASCADE, related_name='journal_account')
    people_for_from = models.ForeignKey(
        People, on_delete=models.CASCADE, related_name='journal_people_for')
    people_by = models.ForeignKey(
        People, on_delete=models.CASCADE, related_name='journal_people_by')
    particular = models.TextField(blank=True)
    debit = models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2, blank=True)
    credit = models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2, blank=True)

    def __str__(self):
        return self.voucher_no


class Transaction(models.Model):
    date = models.DateField()
    trnsaction_type = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=False)
    account = models.ForeignKey(
        CreateAccount, on_delete=models.CASCADE, related_name='transaction_account')
    total_debit = models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2)
    total_credit = models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2)
    balance = models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2)
