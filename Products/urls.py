from Products import views
from django.urls import path


app_name = 'Products'

urlpatterns = [
    path('add-product/', views.add_product, name='add_product'),
]
