from Purchases import views
from django.urls import path


app_name = 'Purchase'

urlpatterns = [
    path('add-expense/', views.add_expense, name='add_expense'),
]
