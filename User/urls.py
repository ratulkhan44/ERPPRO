from User import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'User'

urlpatterns = [
    path('user-role/', views.user_role, name='user_role'),
    path('create-user/', views.create_user, name='create_user'),
    path('activate/<uidb64>/<token>/',
         views.ActivateAccount.as_view(), name='activate'),
    path('employee/dashboard/', views.employee_dashboard,
         name='employee_dashboard'),
    path('supervisor/dashboard/', views.supervisor_dashboard,
         name='supervisor_dashboard'),
    path('supervisor/petty-expense/', views.supervisior_petty_cash_expense,
         name='supervisior_petty_cash_expense'),
    path('supervisor/petty-expense-accept/<int:id>',
         views.supervisior_petty_cash_expense_accept, name='supervisior_petty_cash_expense_accept'),
    path('accounts/dashboard/', views.accounts_dashboard,
         name='accounts_dashboard'),
    path('accounts/petty-expense/', views.accounts_petty_cash_expense,
         name='accounts_petty_cash_expense'),
    path('accounts/petty-expense-accept/<int:id>',
         views.accounts_petty_cash_expense_accept, name='accounts_petty_cash_expense_accept'),
    path('accounts/petty-expense-accept-recheck/', views.accounts_petty_cash_expense_accept_recheck,
         name='accounts_petty_cash_expense_accept_recheck'),
    path('accounts_petty_cash_expense_accept_recheck_approve/<int:id>',
         views.accounts_petty_cash_expense_accept_recheck_approve, name='accounts_petty_cash_expense_accept_recheck_approve'),
    path('executive/dashboard/', views.executive_dashboard,
         name='executive_dashboard'),
    path('executive/petty-expense/', views.executive_petty_cash_expense,
         name='executive_petty_cash_expense'),
    path('executive/petty-expense-accept/<int:id>',
         views.executive_petty_cash_expense_accept, name='executive_petty_cash_expense_accept'),


    # Password reset urls

    #     # Password reset urls
    #     path('password-reset/', auth_views.PasswordResetView.as_view(
    #         template_name="Registration/password_reset.html"), name="reset_password"),

    #     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    #         template_name="Registration/password_reset_sent.html"), name="password_reset_done"),

    #     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #         template_name="Registration/password_reset_form.html"), name="password_reset_confirm"),

    #     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
    #         template_name="Registration/password_reset_done.html"), name="password_reset_complete"),

]
