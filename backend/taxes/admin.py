from django.contrib import admin
from .models import IncomeTaxTransactionsModel


class IncomeTaxTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount')


admin.site.register(IncomeTaxTransactionsModel, IncomeTaxTransactionsAdmin)
