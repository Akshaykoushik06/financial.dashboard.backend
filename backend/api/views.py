from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TodoSerializer
from .models import Todo
from django.http import HttpResponse, JsonResponse

# Create your views here.

class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

def returnNetWorth(request):
    res = {
        'netWorth': 18000,
        'assets': {
            'totalAssets': 1900.01,
            'liquidAssets': 1350.02,
            'fixedAssets': 635.03,
            'bankAccounts': {
                'icici': 2500.04,
                'hdfc': 2500.25,
                'iob': 2500.06,
                'canara': 250.07
            },
            'stocks': {
                'invested': 2000.08,
                'curValue': 2500.09,
                'profitLoss': 500.10
            },
            'mutualFunds': {
                'invested': 1500.11,
                'curValue': 1400.12,
                'profitLoss': 100.13
            },
            'gold': {
                'invested': 1500.00,
                'curValue': 1650.00,
                'profitLoss': 150.00
            },
            'providentFund': {
                'value': 2350.00
            },
            'foodCard': {
                'value': 1500.26
            }
        },
        'liabilities': {
            'totalLiability': 10000.19,
            'loans': {
                'twoWheelerLoan': 5900.01
            },
            'creditCards': {
                'dinersClub': 1501.02
            },
            'incomeTax': {
                'tax': 3500.17
            }
        }
    }
    return JsonResponse(res)
