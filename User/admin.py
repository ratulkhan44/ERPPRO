from django.contrib import admin

# Register your models here.
from .models import CustomUser, UserRole

admin.site.register(CustomUser)
admin.site.register(UserRole)
