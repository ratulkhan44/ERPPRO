from django.contrib import admin

# Register your models here.
from .models import (Bill, BillItem, BillPayment, Customer, PurchaseItem,
                     PurchaseOrder, Vendor)

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseItem)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(BillPayment)
