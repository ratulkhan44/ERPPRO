from decimal import Decimal

from Accountant.models import CreateAccount
from django.db import models
from Products.models import Product
from User.models import CustomUser

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(
        max_length=100, blank=True, null=True)
    contact = models.BigIntegerField(null=True, blank=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    opening_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


PURCHASE_STATUS = (
    ('Draft', 'Draft'),
    ('Pending', 'Pending'),
    ('Checked', 'Checked'),
    ('Approved', 'Approved'),
    ('Invoiced', 'Invoiced'),
    ('Billed', 'Billed')
)

BILL_STATUS = (
    ('Draft', 'Draft'),
    ('Pending', 'Pending'),
    ('Checked', 'Checked'),
    ('Approved', 'Approved'),
    ('Invoiced', 'Invoiced')
)


class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='order_vendor')
    order_no = models.CharField(max_length=255)
    reference = models.CharField(blank=True, null=True, max_length=100)
    order_date = models.DateField()
    status = models.CharField(choices=PURCHASE_STATUS,
                              max_length=50, default='Draft')
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='order_created_by')
    is_supervisor = models.BooleanField(default=False)
    is_executive = models.BooleanField(default=False)
    approved_supervisor = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='purchase_approved_supervisor', null=True)
    approved_executive = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='purchase_approved_executive', null=True)

    def __str__(self):
        return self.order_no

    def get_total_amount(self):
        return sum(item.item_amount for item in self.order_item.all())


class PurchaseItem(models.Model):
    item_name = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name='purchase_item')
    item_price = models.CharField(blank=False, null=False, max_length=100)
    item_unit = models.CharField(blank=False, null=False, max_length=100)
    item_quantity = models.CharField(blank=False, null=False, max_length=100)
    item_discount = models.CharField(blank=False, null=False, max_length=100)
    item_amount = models.DecimalField(
        blank=False, null=False, max_digits=10, decimal_places=2)
    purchase_order_item = models.ForeignKey(
        PurchaseOrder, on_delete=models.DO_NOTHING, related_name='order_item')

    def __str__(self):
        return self.item_name


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(unique=True)
    customer_contact_no = models.BigIntegerField(unique=True)
    customer_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.customer_name


class Bill(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='bill_vendor')
    bill_no = models.CharField(max_length=255)
    reference = models.CharField(blank=True, null=True, max_length=100)
    bill_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(choices=BILL_STATUS,
                              max_length=50, default='Draft')
    notes = models.TextField(blank=True, null=True)
    # attached = models.FileField(upload_to="bill_image/", null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='bill_created_by')
    is_employee = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_executive = models.BooleanField(default=False)
    approved_employee = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='bill_approved_employee', null=True)
    approved_supervisor = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='bill_approved_supervisor', null=True)
    approved_executive = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='bill_approved_executive', null=True)

    def __str__(self):
        return self.bill_no

    def get_total_amount(self):
        return sum(item.item_amount for item in self.bill_item.all())


class BillItem(models.Model):
    item_name = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name='bill_item_name')
    item_price = models.CharField(blank=False, null=False, max_length=100)
    item_unit = models.CharField(blank=False, null=False, max_length=100)
    item_quantity = models.CharField(blank=False, null=False, max_length=100)
    item_discount = models.CharField(blank=False, null=False, max_length=100)
    item_amount = models.DecimalField(
        blank=False, null=False, max_digits=10, decimal_places=2)
    bill_item = models.ForeignKey(
        Bill, on_delete=models.DO_NOTHING, related_name='bill_item')
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='bill_customer')

    def __str__(self):
        return self.item_name


class BillPayment(models.Model):
    bill=models.ForeignKey(
        Bill, on_delete=models.CASCADE, related_name='bill_payment')
    amount = models.DecimalField(
        blank=False, null=False, max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_made=models.CharField(max_length=200,null=True,blank=True)
    payment_through=models.ForeignKey(
        CreateAccount, on_delete=models.CASCADE, related_name='payment_account')
    reference= models.CharField(max_length=200,null=True,blank=True)
    notes = models.TextField(blank=True, null=True)
    #attached 

    def __str__(self):
        return str(self.amount)  


