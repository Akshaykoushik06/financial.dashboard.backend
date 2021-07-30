from django.contrib import admin
from .models import LoansTransactionsModel


class LoansTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount')


admin.site.register(LoansTransactionsModel, LoansTransactionsAdmin)
