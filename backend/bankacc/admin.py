from django.contrib import admin
from .models import ICICITransactionsModel, HDFCTransactionsModel, IOBTransactionsModel, CanaraTransactionsModel


class ICICITransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'credit')


class HDFCTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'credit')


class IOBTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'credit')


class CanaraTransactionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'credit')


admin.site.register(ICICITransactionsModel, ICICITransactionsAdmin)
admin.site.register(HDFCTransactionsModel, HDFCTransactionsAdmin)
admin.site.register(IOBTransactionsModel, IOBTransactionsAdmin)
admin.site.register(CanaraTransactionsModel, CanaraTransactionsAdmin)
