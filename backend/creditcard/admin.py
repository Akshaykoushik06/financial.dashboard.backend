from django.contrib import admin
from .models import CreditCardTransactionsModel


class CreditCardTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'billPaid', 'type_of_txn')


admin.site.register(CreditCardTransactionsModel, CreditCardTransactionsAdmin)
