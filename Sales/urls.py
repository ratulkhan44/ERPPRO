from Sales import views
from django.urls import path


app_name = 'Sales'

urlpatterns = [
    path('sales/', views.sales, name='sales'),
    path('cash/', views.cash, name='cash'),
    path('customer/', views.customer, name='customer'),
]
