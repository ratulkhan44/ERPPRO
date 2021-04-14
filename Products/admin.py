from django.contrib import admin

# Register your models here.
from .models import Inventory, Product

admin.site.register(Product)
admin.site.register(Inventory)
