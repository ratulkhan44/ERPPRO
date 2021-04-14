from django.shortcuts import render
from Products.models import Product, Inventory
from django.contrib import messages
from Products import forms
from Accountant.models import BaseAccount, AccountType, CreateAccount
from django.db.models import Q
from itertools import chain

# Create your views here.


def create_product(request):
    form = forms.ProductForm

    inventory_product_form = forms.InventoryProductForm

    if request.method == 'POST':
        form = forms.ProductForm(request.POST)
        inventory_product_form = forms.InventoryProductForm(request.POST)

        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully')

        if request.POST.get('track_inventory') == 'on' and inventory_product_form.is_valid():
            inventory_product_form = inventory_product_form.save(commit=False)
            inventory_product_form.product = product
            inventory_product_form.save()
            messages.success(request, 'Product added successfully')

    return render(request, 'products/add_product.html', {'form': form, 'inventory_product_form': inventory_product_form})
