from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import include, path
from User import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('permission-denied/', views.permission_denied, name='permission_denied'),
    # Password reset urls
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name="Registration/password_reset.html"), name="reset_password"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="Registration/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="Registration/password_reset_form.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="Registration/password_reset_complete.html"), name="password_reset_complete"),
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),
    path('sales/', include('Sales.urls')),
    path('accountant/', include('Accountant.urls')),
    path('purchases/', include('Purchases.urls')),
    path('people/', include('People.urls')),
    path('products/', include('Products.urls')),
    path('expense/', include('Expense.urls')),
    path('reports/', include('Reports.urls')),
    path('settings/', include('Settings.urls')),


]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
