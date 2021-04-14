from django import forms
from  Products.models import Product_Type, Product, Unit_Choices, Inventory
from Accountant.models import CreateAccount

class ProductForm(forms.ModelForm):
    selling_accounts = CreateAccount.objects.filter(account_type__base_account__base_account="Income")
    cost_accounts = CreateAccount.objects.filter(account_type__account_type="COGS")
    

    product_type=  forms.ChoiceField(required = True, choices=Product_Type, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'product_type'}))
    product_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control product_name', 'id': 'product_name'}))
    unit = forms.ChoiceField(required=False, choices=Unit_Choices, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'unit'}))
    selling_price = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'selling_price'}))
    selling_account = forms.ModelChoiceField(queryset=selling_accounts,required=False, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'selling_account'}))
    selling_description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'selling_description'}))
    cost_price = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'cost_price'}))
    cost_account = forms.ModelChoiceField(queryset=cost_accounts,required=False, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'cost_account'}))
    cost_description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'cost_description'}))
    track_inventory = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control', 'id': 'track_inventory'}))
    
    

    class Meta:
        model = Product
        fields = '__all__'
        
class InventoryProductForm(forms.ModelForm):
    inventory_accounts = CreateAccount.objects.filter(account_name="Inventory")
    inventory_account = forms.ModelChoiceField(queryset=inventory_accounts,required=False, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'inventory_account'}))
    opening_stock = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'opening_stock'}))
    opening_stock_rate_per_unit = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'opening_stock_rate_per_unit'}))

    class Meta:
        model = Inventory
        exclude = ('product',)
