from django.contrib import admin
from .models import PFTransactionsModel


class PFTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount')


admin.site.register(PFTransactionsModel, PFTransactionsAdmin)
