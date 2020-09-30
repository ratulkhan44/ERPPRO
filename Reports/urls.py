from Reports import views
from django.urls import path


app_name = 'Reports'

urlpatterns = [
    path('allreports', views.allreports, name='allreports'),
    path('general-ledger', views.general_ledger, name='general_ledger'),
    path('journal-report', views.journal_report, name='journal_report'),
    path('balance-sheet', views.balance_sheet, name='balance_sheet'),
    path('account-transactions/<int:id>', views.account_transactions,
         name='account_transactions'),
]
