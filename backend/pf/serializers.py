from rest_framework import serializers
from .models import PFTransactionsModel


class PFTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PFTransactionsModel
        fields = ('_id', 'amount', 'date', 'description')
