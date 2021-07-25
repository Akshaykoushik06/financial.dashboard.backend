from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CreditCardTransactionsSerializer
from .models import CreditCardTransactionsModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from api.models import HomePageModel
from api.serializers import HomePageSerializer
import datetime


def calculate_bill(serialized_data):
    res = {
        'current_statement_txns': serialized_data,
        'amount': 0,
        'last_paid_bill': None
    }
    for txn in serialized_data:
        for k, v in txn.items():
            if k == 'type_of_txn':
                if v == 'debit':
                    res['amount'] += float(txn['amount'])
                if v == 'credit':
                    res['amount'] -= float(txn['amount'])
                if v == 'bill':
                    res['last_paid_bill'] = txn
    return res


@api_view(['GET'])
def getCreditCardTxns(request):
    # Calculating amount to pay line no. 38 - 46
    # find the range
    currentTimestamp = datetime.datetime.now()
    start_date = datetime.date(
        currentTimestamp.year, currentTimestamp.month - 1, 17)
    end_date = datetime.date(currentTimestamp.year, currentTimestamp.month, 16)

    # query the db on the date range calculated
    txns = CreditCardTransactionsModel.objects.filter(
        date__range=(start_date, end_date)).order_by('-date')
    serializer = CreditCardTransactionsSerializer(txns, many=True)

    result = calculate_bill(serializer.data)

    # Calculating unbilled txns line no. 52 - 58
    # current month 17 - next month 16 => unbilled txn
    start_date = datetime.date(
        currentTimestamp.year, currentTimestamp.month, 17)
    end_date = datetime.date(currentTimestamp.year,
                             currentTimestamp.month + 1, 16)

    txns = CreditCardTransactionsModel.objects.filter(
        date__range=(start_date, end_date)).order_by('-date')
    serializer = CreditCardTransactionsSerializer(txns, many=True)
    result['unbilled_txns'] = serializer.data

    return Response(result, status=status.HTTP_200_OK)


@api_view(['PUT'])
def editTxnEntry(request):
    updatedTxnEntry = {
        'amount': request.data['amount'],
        'date': request.data['date'],
        'description': request.data['description'],
        'billPaid': request.data['billPaid'],
        'type_of_txn': request.data['type_of_txn']
    }
    txn = CreditCardTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    serializer = CreditCardTransactionsSerializer(
        instance=txn, data=updatedTxnEntry)
    if serializer.is_valid():
        serializer.save()
    return Response('EDIT TXN - SUCCESS', status=status.HTTP_200_OK)


@api_view(['POST'])
def createTxnEntry(request):
    request.data['billPaid'] = False
    serializer = CreditCardTransactionsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response('CREATE TXN - SUCCESS', status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteTxnEntry(request):
    txn = CreditCardTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    txn.delete()
    return Response('DELETE TXN - SUCCESS', status=status.HTTP_200_OK)
