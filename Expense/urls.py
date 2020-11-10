from Expense import views
from django.urls import path


app_name = 'Expense'

urlpatterns = [
    path('expense-requisition/', views.expense_requisition,
         name='expense_requisition'),
]
