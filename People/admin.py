from django.contrib import admin

# Register your models here.
from .models import Company, Department, People

admin.site.register(People)
admin.site.register(Company)
admin.site.register(Department)

