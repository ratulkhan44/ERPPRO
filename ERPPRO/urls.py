from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from Sales import views
from People import views
from Reports import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/', include('Sales.urls')),
    path('accountant/', include('Accountant.urls')),
    path('people/', include('People.urls')),
    path('reports/', include('Reports.urls')),

]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
