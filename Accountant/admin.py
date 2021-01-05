from django.contrib import admin
from .models import BaseAccount, AccountType, CreateAccount, ManualJournal

# Register your models here.

admin.site.register(BaseAccount)
admin.site.register(AccountType)
admin.site.register(CreateAccount)
admin.site.register(ManualJournal)
