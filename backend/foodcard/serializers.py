from rest_framework import serializers
from .models import FoodCardTransactionsModel


class FoodCardTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCardTransactionsModel
        fields = ('_id', 'amount', 'date', 'description', 'credit')
