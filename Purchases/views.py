import datetime
import decimal
import json
from itertools import chain

from Accountant.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from Products.models import Inventory, Product
from User.decorators import required_role

from Purchases import forms
from Purchases.models import (Bill, BillItem, Customer, PurchaseItem,
                              PurchaseOrder)

from .models import Vendor

# Create your views here.


def add_expense(request):
    # (baseAccount.objects.filter(Q(base_account__iexact=account) & Q(accounttype_baseaccount__createaccount_account_type__transaction_account__date__range=[
    #     start_date, end_date])).aggregate(sum_total=(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_debit))-(Sum('accounttype_baseaccount__createaccount_account_type__transaction_account__'+transaction_credit)))['sum_total']) or 0
    paid_accounts = CreateAccount.objects.filter(
        Q(account_name__iexact='Cash') | Q(account_name__iexact='Bank A/C')).order_by('id')
    expense_accounts = CreateAccount.objects.filter(Q(account_type_id=7) | Q(account_type_id=8) | Q(account_type_id=9) | Q(
        account_type_id=10) | Q(account_type_id=11) | Q(account_type_id=12) | Q(account_type_id=13) | Q(account_type_id=14))
    peoples = People.objects.all()

    return render(request, 'purchases/add_expense.html', context={'expense_accounts': expense_accounts, 'paid_accounts': paid_accounts, 'peoples': peoples})


def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'purchases/vendor_list.html', context={'vendors': vendors})


def create_vendor(request):
    form = forms.VendorForm

    if request.method == 'POST':
        form = forms.VendorForm(request.POST)
        # import pdb
        # pdb.set_trace()

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Vendor Created Successfully')
            return HttpResponseRedirect(reverse('Purchase:create_vendor'))

    return render(request, 'purchases/create_vendor.html', context={'form': form})


def increment_order_no():
    last_order = PurchaseOrder.objects.all().order_by('id').last()
    if not last_order:
        return 'PO-000001'
    order_no = last_order.order_no
    order_int = int(order_no.split('PO-')[-1])
    width = 6
    new_order_int = order_int + 1
    formatted = (width - len(str(new_order_int))) * "0" + str(new_order_int)
    new_order_no = 'PO-' + str(formatted)
    # import pdb
    # pdb.set_trace()
    return new_order_no


def show_price(request, id):
    products = Product.objects.filter(id=id)
    inventories = Inventory.objects.filter(product_id=id)
    rate_quantity = list(chain(products, inventories))
    rateSerializer = serializers.serialize('json', rate_quantity)
    return HttpResponse(rateSerializer, content_type='application/json')


def show_order_no(request):
    order_no = increment_order_no()
    order_dic = {
        'order_no': order_no
    }
    get_order = json.dumps(order_dic)
    return HttpResponse(get_order, content_type='application/json')


def show_bill_no(request):
    bill_no = increment_bill_no()
    bill_dic = {
        'bill_no': bill_no
    }
    get_bill = json.dumps(bill_dic)
    return HttpResponse(get_bill, content_type='application/json')


def create_purchase_order(request):
    vendors = Vendor.objects.all()
    products = Product.objects.all()
    context = {
        'vendors': vendors,
        'products': products
    }
    if request.method == "POST":
        my_data = json.loads(request.body)
        vendor_name = my_data['vendor_name']
        order_date = my_data['order_date']
        purchase_order = my_data['purchase_order']
        reference = my_data['reference']
        purchase = PurchaseOrder.objects.create(
            vendor_id=vendor_name, order_date=order_date, order_no=purchase_order, reference=reference, created_by_id=request.user.id)
        purchase.save()
        get_purchase = PurchaseOrder.objects.get(id=purchase.id)

        for item in my_data["items"]:
            item_name = item['item_name']
            item_price = item['item_price']
            item_quantity = item['item_quantity']
            item_unit = item['item_unit']
            item_amount = item['item_amount']
            item_discount = item['item_discount']
            PurchaseItem.objects.create(item_price=item_price, item_quantity=item_quantity, item_discount=item_discount, item_amount=item_amount, item_name_id=item_name,
                                        item_unit=item_unit,   purchase_order_item_id=get_purchase.id)
        messages.success(request, 'Purchase Order Created Successfully')
        return render(request, 'purchases/create_purchase_order.html', context)

    return render(request, 'purchases/create_purchase_order.html', context)


def purchase_order_list(request):
    if str(request.user.user_role) == 'Employee':
        order_lists = PurchaseOrder.objects.filter(
            created_by_id=request.user.id)
        return render(request, 'purchases/purchase_order_list.html', {'order_lists': order_lists})
    elif str(request.user.user_role) == 'Supervisor':
        order_lists = PurchaseOrder.objects.filter(
            Q(status="Pending") | Q(status="Checked") | Q(created_by_id=request.user.id))
        return render(request, 'purchases/purchase_order_list.html', {'order_lists': order_lists})
    elif str(request.user.user_role) == 'Executive':
        order_lists = PurchaseOrder.objects.filter(
            Q(status="Approved") | Q(status="Checked") | Q(status="Billed") | Q(created_by_id=request.user.id))
        return render(request, 'purchases/purchase_order_list.html', {'order_lists': order_lists})
    elif str(request.user.user_role) == 'Superadmin':
        order_lists = PurchaseOrder.objects.all()
        return render(request, 'purchases/purchase_order_list.html', {'order_lists': order_lists})
    return render(request, 'purchases/purchase_order_list.html')


def purchase_order_details(request, id):
    order = PurchaseOrder.objects.get(id=id)
    if str(request.user.user_role) == 'Employee':
        if order.created_by_id == request.user.id:
            purchase_items = PurchaseItem.objects.filter(
                purchase_order_item_id=id)
            context = {'purchase_items': purchase_items,
                       'purchase_id': id, 'order': order}
            return render(request, 'purchases/purchase_order_details.html', context)
        else:
            return redirect('permission_denied')
    elif str(request.user.user_role) == 'Supervisor':
        if (order.status == 'Pending' and order.is_supervisor == False) or (order.status == 'Checked' and order.is_supervisor == True) or (order.created_by_id == request.user.id):
            purchase_items = PurchaseItem.objects.filter(
                purchase_order_item_id=id)
            context = {'purchase_items': purchase_items,
                       'purchase_id': id, 'order': order}
            return render(request, 'purchases/purchase_order_details.html', context)
        else:
            return redirect('permission_denied')
    elif str(request.user.user_role) == 'Executive':
        if (order.status == 'Checked' and order.is_supervisor == True) or (order.created_by_id == request.user.id) or (order.status == 'Approved'):
            purchase_items = PurchaseItem.objects.filter(
                purchase_order_item_id=id)
            context = {'purchase_items': purchase_items,
                       'purchase_id': id, 'order': order}
            return render(request, 'purchases/purchase_order_details.html', context)
        else:
            return redirect('permission_denied')
    else:
        purchase_items = PurchaseItem.objects.filter(purchase_order_item_id=id)
        context = {'purchase_items': purchase_items, 'purchase_id': id}
        return render(request, 'purchases/purchase_order_details.html', context)


def purchase_order_edit(request, id):
    order = PurchaseOrder.objects.filter(id=id)
    purchase_items = PurchaseItem.objects.filter(purchase_order_item_id=id)
    purchase_orders = list(chain(order, purchase_items))
    purchaseSerializer = serializers.serialize('json', purchase_orders)
    return HttpResponse(purchaseSerializer, content_type='application/json')


def purchase_order_update(request, id):
    order_id = id
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors,
        'products': products,
        'order_id': order_id
    }
    update_purchase_order = PurchaseOrder.objects.get(id=id)
    update_item = PurchaseItem.objects.filter(purchase_order_item_id=id)

    if request.method == "POST":
        my_data = json.loads(request.body)
        update_purchase_order.vendor_id = my_data['vendor_name']
        update_purchase_order.order_date = my_data['order_date']
        update_purchase_order.reference = my_data['reference']
        update_purchase_order.save()

        if update_item.exists():
            for item in (update_item.iterator()):
                item.delete()

            for item in my_data["items"]:

                item_name = item['item_name']
                item_price = item['item_price']
                item_quantity = item['item_quantity']
                item_unit = item['item_unit']
                item_discount = item['item_discount']
                item_amount = item['item_amount']
                item_order_id = update_purchase_order.id

                PurchaseItem.objects.create(item_price=item_price, item_quantity=item_quantity, item_discount=item_discount, item_amount=item_amount, item_name_id=item_name,
                                            item_unit=item_unit, purchase_order_item_id=item_order_id)

    return render(request, 'purchases/purchase_order_edit.html', context)

# PO--Employee Functionality


@login_required
@required_role(allowed_roles=['Employee', 'Supervisor', 'Executive'])
def employee_submit_for_approval_po(request, id):
    order_list = PurchaseOrder.objects.get(id=id)
    if order_list:
        order_list.status = "Pending"
        order_list.save()
        messages.success(request, 'Purchase Order Submit Successfully')
    return HttpResponseRedirect(reverse('Purchase:purchase_order_list'))

# PO--Supervisor Functionality


@login_required
@required_role(allowed_roles=['Supervisor', 'Executive'])
def supervisor_checked_po(request, id):
    order_list = PurchaseOrder.objects.get(id=id)
    if order_list:
        order_list.status = "Checked"
        order_list.is_supervisor = True
        order_list.approved_supervisor_id = request.user.id
        order_list.save()
        messages.success(request, 'Purchase Order Checked Successfully')
    return HttpResponseRedirect(reverse('Purchase:purchase_order_list'))

# PO--Executive Functionality


@login_required
@required_role(allowed_roles=['Executive'])
def executive_approved_po(request, id):
    order_list = PurchaseOrder.objects.get(id=id)
    if order_list:
        order_list.status = "Approved"
        order_list.is_executive = True
        order_list.approved_executive_id = request.user.id
        order_list.save()
        messages.success(request, 'Purchase Order Approved Successfully')
    return HttpResponseRedirect(reverse('Purchase:purchase_order_list'))

# Billing Functionality


def increment_bill_no():
    last_bill = Bill.objects.all().order_by('id').last()
    if not last_bill:
        return 'BILL-000001'
    bill_no = last_bill.bill_no
    bill_int = int(bill_no.split('BILL-')[-1])
    width = 6
    new_bill_int = bill_int + 1
    formatted = (width - len(str(new_bill_int))) * "0" + str(new_bill_int)
    new_bill_no = 'BILL-' + str(formatted)
    return new_bill_no


def create_bill(request):
    order_id = id
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    customers = Customer.objects.all()
    context = {
        'vendors': vendors,
        'customers': customers,
        'products': products,
        'order_id': order_id
    }

    if request.method == "POST":
        my_data = json.loads(request.body)
        vendor = my_data['vendor_name']
        bill_date = my_data['bill_date']
        due_date = my_data['due_date']
        bill_no = my_data['bill_no']
        reference = my_data['reference']
        notes = my_data['notes']
        created_by = request.user.id

        bill = Bill.objects.create(vendor_id=vendor, bill_date=bill_date, due_date=due_date,
                                   bill_no=bill_no, reference=reference, notes=notes, created_by_id=created_by)

        for item in my_data["items"]:

            item_name = item['item_name']
            item_price = item['item_price']
            item_quantity = item['item_quantity']
            item_unit = item['item_unit']
            item_discount = item['item_discount']
            item_amount = item['item_amount']
            customer_id = item['customer']
            item_order_id = bill.id

            BillItem.objects.create(item_price=item_price, item_quantity=item_quantity, item_discount=item_discount, item_amount=item_amount, item_name_id=item_name,
                                    item_unit=item_unit, customer_id=customer_id, bill_item_id=item_order_id)
    return render(request, 'purchases/create_bill.html', context)


def convert_to_bill(request, id):
    order_id = id
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    customers = Customer.objects.all()
    context = {
        'vendors': vendors,
        'customers': customers,
        'products': products,
        'order_id': order_id
    }

    if request.method == "POST":
        my_data = json.loads(request.body)
        order = PurchaseOrder.objects.get(id=id)
        if order:
            order.status = 'Billed'
            order.save()
        vendor = my_data['vendor_name']
        bill_date = my_data['bill_date']
        due_date = my_data['due_date']
        bill_no = my_data['bill_no']
        reference = my_data['reference']
        notes = my_data['notes']
        created_by = request.user.id

        bill = Bill.objects.create(vendor_id=vendor, bill_date=bill_date, due_date=due_date,
                                   bill_no=bill_no, reference=reference, notes=notes, created_by_id=created_by)

        for item in my_data["items"]:

            item_name = item['item_name']
            item_price = item['item_price']
            item_quantity = item['item_quantity']
            item_unit = item['item_unit']
            item_discount = item['item_discount']
            item_amount = item['item_amount']
            customer_id = item['customer']
            item_order_id = bill.id

            BillItem.objects.create(item_price=item_price, item_quantity=item_quantity, item_discount=item_discount, item_amount=item_amount, item_name_id=item_name,
                                    item_unit=item_unit, customer_id=customer_id, bill_item_id=item_order_id)
    return render(request, 'purchases/convert_bill.html', context)


def bill_list(request):
    bills = Bill.objects.all()
    return render(request, 'purchases/all_bills.html', context={'bills': bills})


def bill_details(request, id):
    bill_items = Bill.objects.get(id=id)
    bill_items = BillItem.objects.filter(bill_item_id=id)
    context = {'bill_items': bill_items, 'bill_id': id}
    return render(request, 'purchases/bill_details.html', context)


def bill_edit(request, id):
    bill = Bill.objects.filter(id=id)
    bill_items = BillItem.objects.filter(bill_item_id=id)
    bill_info = list(chain(bill, bill_items))
    billSerializer = serializers.serialize('json', bill_info)
    return HttpResponse(billSerializer, content_type='application/json')


def bill_update(request, id):
    bill_id = id
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    customers = Customer.objects.all()
    context = {
        'vendors': vendors,
        'products': products,
        'bill_id': bill_id,
        'customers': customers
    }
    update_bill = Bill.objects.get(id=id)
    update_item = BillItem.objects.filter(bill_item_id=id)

    if request.method == "POST":
        my_data = json.loads(request.body)
        import pdb
        pdb.set_trace()
        update_bill.vendor = my_data['vendor_name']
        update_bill.due_date = my_data['due_date']
        update_bill.bill_no = my_data['bill_no']
        update_bill.reference = my_data['reference']
        update_bill.notes = my_data['notes']
        update_bill.save()

        if update_item.exists():
            for item in (update_item.iterator()):
                item.delete()

            for item in my_data["items"]:

                item_name = item['item_name']
                item_price = item['item_price']
                item_quantity = item['item_quantity']
                item_unit = item['item_unit']
                item_discount = item['item_discount']
                item_amount = item['item_amount']
                customer = item['customer']
                item_order_id = update_bill.id

                BillItem.objects.create(item_price=item_price, item_quantity=item_quantity, item_discount=item_discount, item_amount=item_amount, item_name_id=item_name,
                                        item_unit=item_unit, bill_item_id=item_order_id)

    return render(request, 'purchases/edit_bill.html', context)


def executive_submit_for_approval_bill(request, id):
    bill = Bill.objects.get(id=id)
    order_list = PurchaseOrder.objects.get(id=id)
    if bill:
        bill.status = "Pending"
        bill.save()
        messages.success(request, 'Bill Submit Successfully')
    return HttpResponseRedirect(reverse('Purchase:bill_list'))

def convert_payment(request):
    context={}
    return render(request, 'purchases/convert_payment.html', context)

