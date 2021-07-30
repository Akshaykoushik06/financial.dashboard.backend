from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import IncomeTaxTransactionsSerializer
from .models import IncomeTaxTransactionsModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from api.models import HomePageModel
from api.serializers import HomePageSerializer
import datetime


@api_view(['GET'])
def getAllTxns(request):
    res = {
        'tax_for_FY': 50000.00,
        'tax_paid_so_far': 0.00,
        'remaining_tax': 0.00,
        'txns': [],
    }

    txns = IncomeTaxTransactionsModel.objects.all().order_by('-date')
    serializer = IncomeTaxTransactionsSerializer(txns, many=True)

    res['txns'] = serializer.data

    for txn in serializer.data:
        res['tax_paid_so_far'] += float(txn['amount'])

    res['remaining_tax'] = res['tax_for_FY'] - res['tax_paid_so_far']
    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def createTxn(request):
    serializer = IncomeTaxTransactionsSerializer(data=request.data)
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

    txn = IncomeTaxTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    serializer = IncomeTaxTransactionsSerializer(
        instance=txn, data=updatedTxnEntry)

    if serializer.is_valid():
        serializer.save()

    return Response("EDIT TXN - SUCCESS", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delTxn(request):
    txn = IncomeTaxTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    txn.delete()

    return Response("DELETE TXN - SUCCESS", status=status.HTTP_200_OK)
