from rest_framework import serializers
from .models import CreditCardTransactionsModel


class CreditCardTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardTransactionsModel
        fields = ('_id', 'amount', 'date', 'description',
                  'billPaid', 'type_of_txn')
