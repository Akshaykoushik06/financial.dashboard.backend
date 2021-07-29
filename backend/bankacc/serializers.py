from rest_framework import serializers
from .models import ICICITransactionsModel, HDFCTransactionsModel, IOBTransactionsModel, CanaraTransactionsModel


class ICICITransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICICITransactionsModel
        fields = ('_id', 'amount', 'date', 'description',
                  'credit')


class HDFCTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDFCTransactionsModel
        fields = ('_id', 'amount', 'date', 'description',
                  'credit')


class IOBTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IOBTransactionsModel
        fields = ('_id', 'amount', 'date', 'description',
                  'credit')


class CanaraTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanaraTransactionsModel
        fields = ('_id', 'amount', 'date', 'description',
                  'credit')
