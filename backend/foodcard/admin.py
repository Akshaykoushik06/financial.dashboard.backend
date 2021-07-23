from django.contrib import admin
from .models import FoodCardTransactionsModel


class FoodCardTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount')


admin.site.register(FoodCardTransactionsModel, FoodCardTransactionsAdmin)
