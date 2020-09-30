from django.shortcuts import render

# Create your views here.


def sales(request):
    return render(request, 'sales/invoice.html', context={})


def customer(request):
    return render(request, 'sales/customer.html', context={})


def cash(request):
    return render(request, 'accountant/cash.html', context={})
