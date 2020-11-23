from django.db import models
from Accountant.models import CreateAccount
from People.models import People
from User.models import CustomUser

# Create your models here.


class Expense(models.Model):
    expense_date=models.DateField()
    paid_account=models.ForeignKey(
        CreateAccount, on_delete=models.CASCADE, related_name='paid_account')
    expense_account=models.ForeignKey(
        CreateAccount, on_delete=models.CASCADE, related_name='expense_account')
    particular=models.TextField(blank=True)
    people_for=models.ForeignKey(
        People, on_delete=models.CASCADE, related_name='expense_people_for')
    people_by=models.ForeignKey(
        People, on_delete=models.CASCADE, related_name='expense_people_by')
    expense_image=models.ImageField(upload_to="expense_image/", null=True, blank=True)
    is_supervisor=models.BooleanField(default=False)
    is_accounts_first=models.BooleanField(default=False)
    is_accounts_second=models.BooleanField(default=False)
    is_executive=models.BooleanField(default=False)
    amount=models.DecimalField(
        default="0.00", max_digits=12, decimal_places=2, blank=True)
    user=models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='expense_user')
    approved_supervisor=models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='approved_supervisor',null=True)
    approved_accounts=models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='approved_accounts',null=True)
    approved_executive=models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='approved_executive',null=True)    
    
