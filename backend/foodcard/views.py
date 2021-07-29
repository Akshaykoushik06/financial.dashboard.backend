from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FoodCardTransactionsSerializer
from .models import FoodCardTransactionsModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from api.models import HomePageModel
from api.serializers import HomePageSerializer


def updateWalletBalance(isCredit, requestAmount):
    # fetch the current wallet balance
    dbModel = HomePageModel.objects.get(
        _id=ObjectId('60f92d5fac57d496f70f2361'))
    serializer = HomePageSerializer(dbModel)
    fields = ['liabilities_creditCardAmount',
              'icici_balance', 'hdfc_balance', 'iob_balance', 'canara_balance']
    newData = {}
    for field in fields:
        newData[field] = serializer.data[field]
    oldBalance = float(HomePageSerializer(
        dbModel).data['foodCardBalance'])

    # add/subtract from the old balance
    newBalance = (
        oldBalance + requestAmount) if isCredit else (oldBalance - requestAmount)
    newData['foodCardBalance'] = newBalance
    # update the wallet balance
    homePageSerializer = HomePageSerializer(
        instance=dbModel, data=newData)
    if homePageSerializer.is_valid():
        homePageSerializer.save()


@api_view(['GET'])
def getAllFoodCardTransactions(request):
    txns = FoodCardTransactionsModel.objects.all().order_by('-date')
    serializer = FoodCardTransactionsSerializer(txns, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def editTxn(request):
    # update the txn entry
    newData = float(request.data['amount'])
    updatedTxnEntry = {
        'amount': newData,
        'date': request.data['date'],
        'description': request.data['description'],
        'credit': request.data['credit']
    }
    txn = FoodCardTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    oldData = float(FoodCardTransactionsSerializer(txn).data['amount'])
    serializer = FoodCardTransactionsSerializer(
        instance=txn, data=updatedTxnEntry)
    if serializer.is_valid():
        serializer.save()

    # update the wallet balance
    diff = oldData - newData
    if diff != 0:
        updateWalletBalance(not request.data['credit'], diff)
    return Response("UPDATE TRANSACTION - SUCCESS", status=status.HTTP_200_OK)


@api_view(['POST'])
def createNewTxn(request):
    # check if credit/debit
    credit = request.data['credit']

    updateWalletBalance(credit, float(request.data['amount']))

    # save the transaction in txns collection
    foodCardSerializer = FoodCardTransactionsSerializer(data=request.data)
    if foodCardSerializer.is_valid():
        foodCardSerializer.save()
    return Response('ADD TRANSACTION - SUCCESS', status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteTxn(request):
    txn = FoodCardTransactionsModel.objects.get(
        _id=ObjectId(request.data['_id']))
    oldData = FoodCardTransactionsSerializer(txn)
    updateWalletBalance(
        not oldData.data['credit'], float(oldData.data['amount']))
    txn.delete()
    return Response('TXN DELETE - SUCCESS', status=status.HTTP_200_OK)


# The below method is not needed anymore as it is handled on the frontend


@api_view(['GET'])
def getTxnById(request, id):
    txn = FoodCardTransactionsModel.objects.get(_id=ObjectId(id))
    serializer = FoodCardTransactionsSerializer(txn)
    return Response(serializer.data, status=status.HTTP_200_OK)
