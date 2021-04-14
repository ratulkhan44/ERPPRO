from Products import views
from django.urls import path


app_name = 'Products'

urlpatterns = [
    path('add-product/', views.create_product, name='add_product'),
]
