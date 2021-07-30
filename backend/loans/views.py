from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LoansTransactionsSerializer
from .models import LoansTransactionsModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from api.models import HomePageModel
from api.serializers import HomePageSerializer
import datetime


def getLoanAmounts():
    res = {
        'amount_remaining': 110808.00,
        'months_remaining': 24,
        'txns': [],
    }

    amount_paid_so_far = 0.00

    txns = LoansTransactionsModel.objects.all().order_by('-date')
    serializer = LoansTransactionsSerializer(txns, many=True)

    res['txns'] = serializer.data

    for txn in serializer.data:
        res['months_remaining'] -= 1
        res['amount_remaining'] -= float(txn['amount'])
        amount_paid_so_far += float(txn['amount'])

    return amount_paid_so_far, res


@api_view(['GET'])
def getAllTxns(request):
    _, res = getLoanAmounts()
    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def createTxn(request):
    serializer = LoansTransactionsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response("Create txn endpoint working", status=status.HTTP_200_OK)


@api_view(['PUT'])
def editTxn(request):
    updatedTxnEntry = {
        'amount': request.data['amount'],
        'date': request.data['date'],
        'description': request.data['description'],
    }

    txn = LoansTransactionsModel.objects.get(_id=ObjectId(request.data['_id']))
    serializer = LoansTransactionsSerializer(
        instance=txn, data=updatedTxnEntry)

    if serializer.is_valid():
        serializer.save()

    return Response("EDIT TXN - SUCCESS", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delTxn(request):
    txn = LoansTransactionsModel.objects.get(_id=ObjectId(request.data['_id']))
    txn.delete()

    return Response("DELETE TXN - SUCCESS", status=status.HTTP_200_OK)
