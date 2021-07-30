from rest_framework import serializers
from .models import IncomeTaxTransactionsModel


class IncomeTaxTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTaxTransactionsModel
        fields = ('_id', 'amount', 'date', 'description')
