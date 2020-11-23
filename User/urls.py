from User import views
from django.urls import path


app_name = 'User'

urlpatterns = [
    path('user-role/', views.user_role, name='user_role'),
    path('create-user/', views.create_user, name='create_user'),
    path('supervisor/dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('supervisor/petty-expense/', views.supervisior_petty_cash_expense, name='supervisior_petty_cash_expense'),
    path('supervisor/petty-expense-accept/<int:id>', views.supervisior_petty_cash_expense_accept, name='supervisior_petty_cash_expense_accept'),
    path('accounts/dashboard/', views.accounts_dashboard, name='accounts_dashboard'),
    path('accounts/petty-expense/', views.accounts_petty_cash_expense, name='accounts_petty_cash_expense'),
    path('accounts/petty-expense-accept/<int:id>', views.accounts_petty_cash_expense_accept, name='accounts_petty_cash_expense_accept'),
    path('accounts/petty-expense-accept-recheck/', views.accounts_petty_cash_expense_accept_recheck, name='accounts_petty_cash_expense_accept_recheck'),
    path('accounts_petty_cash_expense_accept_recheck_approve/<int:id>',views.accounts_petty_cash_expense_accept_recheck_approve,name='accounts_petty_cash_expense_accept_recheck_approve'),
    path('executive/dashboard/', views.executive_dashboard, name='executive_dashboard'),
    path('executive/petty-expense/', views.executive_petty_cash_expense, name='executive_petty_cash_expense'),
    path('executive/petty-expense-accept/<int:id>', views.executive_petty_cash_expense_accept, name='executive_petty_cash_expense_accept'),
]