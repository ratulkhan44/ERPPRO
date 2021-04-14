from django.urls import path

from Purchases import views

app_name = 'Purchase'

urlpatterns = [
    path('add-expense/', views.add_expense, name='add_expense'),
    path('vendor-list/', views.vendor_list, name='vendor_list'),
    path('create-vendor/', views.create_vendor, name='create_vendor'),
    path('create-purchase-order/', views.create_purchase_order,
         name='create_purchase_order'),
    path('get-order-no/', views.show_order_no, name='show_order_no'),
    path('get-bill-no/', views.show_bill_no, name='show_bill_no'),
    path('create-purchase-order/getrate/<int:id>/',
         views.show_price, name='show_price'),
    path('purchase-order-list/',
         views.purchase_order_list, name='purchase_order_list'),
    path('purchase-order-details/<str:id>/',
         views.purchase_order_details, name='purchase_order_details'),
    path('purchase-order-edit/<str:id>/',
         views.purchase_order_edit, name='purchase_order_edit'),
    path('purchase-order-update/<str:id>/',
         views.purchase_order_update, name='purchase_order_update'),
    path('employee-submit-for-approval-po/<int:id>/',
         views.employee_submit_for_approval_po, name='employee_submit_for_approval_po'),
    path('supervisor-checked-po/<int:id>/',
         views.supervisor_checked_po, name='supervisor_checked_po'),
    path('executive-approved-po/<int:id>/',
         views.executive_approved_po, name='executive_approved_po'),
    # Bill url
    path('create-bill', views.create_bill, name='create_bill'),
    path('convert-to-bill/<int:id>/',
         views.convert_to_bill, name='convert_to_bill'),
    path('bill-list', views.bill_list, name='bill_list'),
    path('bill-details/<str:id>/', views.bill_details, name='bill_details'),
    path('bill-edit/<str:id>/',
         views.bill_edit, name='bill_edit'),
    path('bill-update/<str:id>/',
         views.bill_update, name='bill_update'),
    path('executive-submit-for-approval-bill/<int:id>/',
         views.executive_submit_for_approval_bill, name='executive_submit_for_approval_bill'),
    path('convert-payment', views.convert_payment, name='conver_payment')     

]
