from People import views
from django.urls import path


app_name = 'People'

urlpatterns = [
    path('company-list', views.company_list, name='company_list'),
    path('department-list', views.department_list, name='department_list'),
    path('create-people/', views.create_people, name='create_people'),
    path('people-list/', views.people_list, name='people_list'),
    # path('getdepartment/<pk>/',
    #      views.showDepartment, name='getdepartment')
]
