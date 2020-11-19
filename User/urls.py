from User import views
from django.urls import path


app_name = 'User'

urlpatterns = [
    path('user-role/', views.user_role, name='user_role'),
    path('create-user/', views.create_user, name='create_user'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('executive-dashboard/', views.executive_dashboard, name='executive_dashboard'),
    path('supervisor-dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('supervisor-petty-expense/', views.supervisior_petty_cash_expense, name='supervisior_petty_cash_expense'),
    path('supervisor-petty-expense-accept/<int:id>', views.supervisior_petty_cash_expense_accept, name='supervisior_petty_cash_expense_accept'),
]