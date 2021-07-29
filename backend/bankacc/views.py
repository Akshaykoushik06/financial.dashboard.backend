from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ICICITransactionsSerializer, HDFCTransactionsSerializer, IOBTransactionsSerializer, CanaraTransactionsSerializer
from .models import ICICITransactionsModel, HDFCTransactionsModel, IOBTransactionsModel, CanaraTransactionsModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from api.models import HomePageModel
from api.serializers import HomePageSerializer
import datetime


def updateBankAccBalance(isCredit, requestAmount, bank):
    dbModel = HomePageModel.objects.get(
        _id=ObjectId('60f92d5fac57d496f70f2361'))
    serializer = HomePageSerializer(dbModel)
    fields = ['foodCardBalance', 'liabilities_creditCardAmount',
              'icici_balance', 'hdfc_balance', 'iob_balance', 'canara_balance']
    fields.remove('{0}_balance'.format(bank))
    newData = {}
    for field in fields:
        newData[field] = serializer.data[field]
    # fetch the current wallet balance
    oldBalance = float(HomePageSerializer(
        dbModel).data['{0}_balance'.format(bank)])

    # add/subtract from the old balance
    newBalance = (
        oldBalance + requestAmount) if isCredit else (oldBalance - requestAmount)
    newData['{0}_balance'.format(bank)] = newBalance
    # update the wallet balance
    homePageSerializer = HomePageSerializer(
        instance=dbModel, data=newData)
    # print("New balance", newData, homePageSerializer.is_valid(),
    #       homePageSerializer.errors)

    if homePageSerializer.is_valid():
        homePageSerializer.save()


def getModelAndSerializer(bank):
    mapping = {
        'icici': {
            'model': ICICITransactionsModel,
            'serializer': ICICITransactionsSerializer
        },
        'hdfc': {
            'model': HDFCTransactionsModel,
            'serializer': HDFCTransactionsSerializer
        },
        'iob': {
            'model': IOBTransactionsModel,
            'serializer': IOBTransactionsSerializer
        },
        'canara': {
            'model': CanaraTransactionsModel,
            'serializer': CanaraTransactionsSerializer
        }
    }
    return mapping[bank]['model'], mapping[bank]['serializer']


@api_view(['GET'])
def getBankAccTxns(request, bank):

    res = {
        'balance': 0.0,
        'txns': [],
    }

    model, serializer = getModelAndSerializer(bank)

    txns = model.objects.all().order_by('-date')
    serializer = serializer(txns, many=True)

    homepageModel = HomePageModel.objects.get(
        _id=ObjectId('60f92d5fac57d496f70f2361'))
    balance = float(HomePageSerializer(
        homepageModel).data['{0}_balance'.format(bank)])

    res['balance'] = balance
    res['txns'] = serializer.data

    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def createNewTxnEntry(request, bank):
    # check if credit/debit
    credit = request.data['credit']

    updateBankAccBalance(credit, float(request.data['amount']), bank)

    # save the transaction in txns collection
    model, serializer = getModelAndSerializer(bank)
    serializer = serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response("NET BANK ACC TXN CREATED", status=status.HTTP_200_OK)


@api_view(['PUT'])
def editTxn(request, bank):
    # update the txn entry
    newData = float(request.data['amount'])
    updatedTxnEntry = {
        'amount': newData,
        'date': request.data['date'],
        'description': request.data['description'],
        'credit': request.data['credit']
    }
    model, serializer = getModelAndSerializer(bank)
    txn = model.objects.get(_id=ObjectId(request.data['_id']))
    oldData = float(serializer(txn).data['amount'])
    serializer = serializer(instance=txn, data=updatedTxnEntry)
    if serializer.is_valid():
        serializer.save()

    # update the wallet balance
    diff = oldData - newData
    if diff != 0:
        updateBankAccBalance(not request.data['credit'], diff, bank)
    return Response("UPDATE TXN - SUCCESS", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteTxn(request, bank):
    model, serializer = getModelAndSerializer(bank)
    txn = model.objects.get(_id=ObjectId(request.data['_id']))
    oldData = serializer(txn)
    updateBankAccBalance(
        not oldData.data['credit'], float(oldData.data['amount']), bank)
    txn.delete()
    return Response("DELETE TXN - SUCCESS", status=status.HTTP_200_OK)
