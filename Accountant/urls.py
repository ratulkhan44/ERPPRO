from Accountant import views
from django.urls import path


app_name = 'Accountant'

urlpatterns = [
    path('base-account/', views.base_account, name='base_account'),
    path('account-type/', views.account_type, name='account_type'),
    path('chart-of-accounts/', views.chart_of_accounts, name='chart_of_accounts'),
    path('new-journal/', views.manual_journal, name='new_journal'),
    path('alljournal/', views.all_journal, name='all_journal'),
    path('demojournal/', views.demo_journal, name='demo_journal'),
]
