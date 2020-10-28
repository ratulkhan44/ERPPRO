from People import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


app_name = 'People'

urlpatterns = [
    path('company-list', views.company_list, name='company_list'),
    path('department-list', views.department_list, name='department_list'),
    path('create-people/', views.create_people, name='create_people'),
    path('people-list/', views.people_list, name='people_list'),
    path('validate-username/',csrf_exempt(views.UsernameValidationView.as_view()),name="usernameValidation"),
    path('validate-contact/',csrf_exempt(views.ContactValidationView.as_view()),name="contactValidation"),
    path('validate-nid/',csrf_exempt(views.NidValidationView.as_view()),name="nidValidation"),
    path('validate-passport/',csrf_exempt(views.PassportValidationView.as_view()),name="passportValidation"),
    path('validate-tracking/',csrf_exempt(views.TrackingValidationView.as_view()),name="trackingValidation"),
    path('validate-email/',csrf_exempt(views.EmailValidationView.as_view()),name="emailValidation"),
    path('create-people/getdepartments/<int:id>/', views.show_department, name="comdep")
    # path('getdepartment/<pk>/',
    #      views.showDepartment, name='getdepartment')
]
