from rest_framework import serializers
from .models import Todo, HomePageModel


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('_id', 'title', 'description', 'completed')


class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageModel
        fields = ('_id', 'foodCardBalance', 'liabilities_creditCardAmount',
                  'icici_balance', 'hdfc_balance', 'iob_balance', 'canara_balance')
