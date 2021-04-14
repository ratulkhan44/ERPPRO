from django.db import models
from Accountant.models import CreateAccount

# Create your models here.

Product_Type = (
    ('Goods', 'Goods'),
    ('Fish', 'Fish'),
    ('Others', 'Others'),
)

Unit_Choices = (
    ('Liter', 'Liter'),
    ('Box', 'Box'),
    ('Pcs', 'Pcs'),
    ('cm', 'cm'),
    ('dz', 'dz'),
    ('ft', 'ft'),
    ('g', 'g'),
    ('in', 'in'),
    ('kg', 'kg'),
    ('km', 'km'),
    ('lb', 'lb'),
    ('mg', 'mg'),
    ('m', 'm'),

)


class Product(models.Model):
    product_type = models.CharField(max_length=100, choices=Product_Type)
    product_name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(
        max_length=100, choices=Unit_Choices, blank=False, null=False)
    selling_price = models.FloatField(blank=True, null=True)
    selling_account = models.ForeignKey(
        CreateAccount, related_name='selling_account', on_delete=models.CASCADE, blank=True, null=True)
    selling_description = models.CharField(
        max_length=255, blank=True, null=True)
    cost_price = models.FloatField(blank=True, null=True)
    cost_account = models.ForeignKey(
        CreateAccount, related_name='cost_account', on_delete=models.CASCADE, blank=True, null=True)
    cost_description = models.CharField(max_length=250, blank=True, null=True)
    track_inventory = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class Inventory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_inventory')
    inventory_account = models.ForeignKey(
        CreateAccount, related_name='inventory_account', on_delete=models.CASCADE, blank=True, null=True)
    opening_stock = models.FloatField(blank=True, null=True)
    opening_stock_rate_per_unit = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.product.product_name
