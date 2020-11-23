from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from User import views

urlpatterns = [
    path('',views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('permission-denied/',views.permission_denied,name='permission_denied'),
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),
    path('sales/', include('Sales.urls')),
    path('accountant/', include('Accountant.urls')),
    path('purchases/', include('Purchases.urls')),
    path('people/', include('People.urls')),
    path('products/', include('Products.urls')),
    path('expense/', include('Expense.urls')),
    path('reports/', include('Reports.urls')),

]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
