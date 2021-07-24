from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HomePageSerializer, TodoSerializer
from .models import Todo, HomePageModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId

# TODO-1: Below method can be removed


@api_view(['GET'])
def getfoodCardBalance(request):
    data = HomePageModel.objects.get(_id=ObjectId('60f92d5fac57d496f70f2361'))
    serializer = HomePageSerializer(data)
    return Response(serializer.data['foodCardBalance'], status=status.HTTP_200_OK)

# region


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def getTodos(request):
    if request.method == 'GET':
        # tutorials = Todo.objects.all()
        tutorials = Todo.objects.get(_id=ObjectId('60f725c67bb5234ed0b3f943'))

        # title = request.GET.get('title', None)
        # if title is not None:
        #     tutorials = tutorials.filter(title__icontains=title)

        # tutorials_serializer = TodoSerializer(tutorials, many=True)
        # print('asd', tutorials_serializer.data)
    elif request.method == 'POST':
        # print('asdsd', request.session.exists(request.session.session_key))
        print('asdd', request)
        tutorial_serializer = TodoSerializer(data=request.data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
        # return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        db_data = Todo.objects.get(_id=ObjectId(request.data['_id']))
        serialize = TodoSerializer(instance=db_data, data=request.data)
        if serialize.is_valid():
            serialize.save()
    elif request.method == 'DELETE':
        db_data = Todo.objects.get(_id=ObjectId(request.data['_id']))
        db_data.delete()

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
    # return JsonResponse(tutorials_serializer.data, safe=False)
    # 'safe=False' for objects serialization

# endregion


# @api_view(['GET'])
# def getFoodCardDetails(request):
#     if request.method == 'GET':
#         details = FoodCard.objects.all()

#         print('asdasd', details)

#         foodcard_serializer = FoodCardSerializer(details, many=True)
#         return JsonResponse(foodcard_serializer.data, safe=False)


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()


@api_view(['GET'])
def returnHomePageData(request):
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
    data = HomePageModel.objects.get(_id=ObjectId('60f92d5fac57d496f70f2361'))
    serializer = HomePageSerializer(data)
    res['assets']['foodCard']['value'] = serializer.data['foodCardBalance']
    return Response(res, status=status.HTTP_200_OK)
