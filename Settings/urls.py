from Settings import views
from django.urls import path


app_name = 'Settings'

urlpatterns = [
    path('opening-balance/', views.opening_balance, name='opening_balance'),
]
