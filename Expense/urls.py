from Expense import views
from django.urls import path


app_name = 'Expense'

urlpatterns = [
    path('new-expense/', views.new_expense,
         name='new_expense'),
    path('all-expense/', views.all_expense,
         name='all_expense'),
]
