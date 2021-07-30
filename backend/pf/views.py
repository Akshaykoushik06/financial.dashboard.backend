from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PFTransactionsSerializer
from .models import PFTransactionsModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from api.models import HomePageModel
from api.serializers import HomePageSerializer
import datetime


def getPFBalanceAndTxns():
    res = {
        'balance': 0.00,
        'txns': [],
    }
    txns = PFTransactionsModel.objects.all().order_by('-date')
    serializer = PFTransactionsSerializer(txns, many=True)

    res['txns'] = serializer.data

    for txn in serializer.data:
        res['balance'] += float(txn['amount'])

    return res


@api_view(['GET'])
def getAllTxns(request):
    return Response(getPFBalanceAndTxns(), status=status.HTTP_200_OK)


@api_view(['POST'])
def createTxn(request):
    serializer = PFTransactionsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response("CREATE TXN - SUCCESSFUL", status=status.HTTP_200_OK)


@api_view(['PUT'])
def editTxn(request):
    updatedTxnEntry = {
        'amount': request.data['amount'],
        'date': request.data['date'],
        'description': request.data['description'],
    }

    txn = PFTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    serializer = PFTransactionsSerializer(
        instance=txn, data=updatedTxnEntry)

    if serializer.is_valid():
        serializer.save()

    return Response("EDIT TXN - SUCCESS", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delTxn(request):
    txn = PFTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    txn.delete()

    return Response("DELETE TXN - SUCCESS", status=status.HTTP_200_OK)
