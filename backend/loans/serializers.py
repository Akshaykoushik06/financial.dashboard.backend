from rest_framework import serializers
from .models import LoansTransactionsModel


class LoansTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoansTransactionsModel
        fields = ('_id', 'amount', 'date', 'description')
