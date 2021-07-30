from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HomePageSerializer, TodoSerializer
from .models import Todo, HomePageModel
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
import datetime

from pf.views import getPFBalanceAndTxns
from loans.views import getLoanAmounts
from taxes.views import getTaxes
from creditcard.models import CreditCardTransactionsModel
from creditcard.serializers import CreditCardTransactionsSerializer
from creditcard.views import calculate_bill

# TODO-1: Below method can be removed


@api_view(['GET'])
def getfoodCardBalance(request):
    data = HomePageModel.objects.get(_id=ObjectId('60f92d5fac57d496f70f2361'))
    serializer = HomePageSerializer(data)
    return Response(serializer.data['foodCardBalance'], status=status.HTTP_200_OK)


@api_view(['GET'])
def getCreditCardAmount(request):
    data = HomePageModel.objects.get(_id=ObjectId('60f92d5fac57d496f70f2361'))
    serializer = HomePageSerializer(data)
    return Response(serializer.data['liabilities_creditCardAmount'], status=status.HTTP_200_OK)

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
    # res = {
    #     'netWorth': 18000,
    #     'assets': {
    #         'totalAssets': 1900.01,
    #         'liquidAssets': 1350.02,
    #         'fixedAssets': 635.03,
    #         'bankAccounts': {
    #             'icici': 2500.04,
    #             'hdfc': 2500.25,
    #             'iob': 2500.06,
    #             'canara': 250.07
    #         },
    #         'stocks': {
    #             'invested': 2000.08,
    #             'curValue': 2500.09,
    #             'profitLoss': 500.10
    #         },
    #         'mutualFunds': {
    #             'invested': 1500.11,
    #             'curValue': 1400.12,
    #             'profitLoss': 100.13
    #         },
    #         'gold': {
    #             'invested': 1500.00,
    #             'curValue': 1650.00,
    #             'profitLoss': 150.00
    #         },
    #         'providentFund': {
    #             'value': 2350.00
    #         },
    #         'foodCard': {
    #             'value': 1500.26
    #         }
    #     },
    #     'liabilities': {
    #         'totalLiability': 10000.19,
    #         'loans': {
    #             'twoWheelerLoan': 5900.01
    #         },
    #         'creditCards': {
    #             'dinersClub': 1501.02
    #         },
    #         'incomeTax': {
    #             'tax': 3500.17
    #         }
    #     }
    # }
    '''
    fields available in homepage model and thus can be directly fetched:
    icici_balance, hdfc_balance, iob_balance, canara_balance, foodCardBalance
    credit_card_statement -> dummy. just sitting there in db
    '''

    res = {
        'assets': {
            'bankAccounts': {
                'icici_balance': 0.00,
                'hdfc_balance': 0.00,
                'iob_balance': 0.00,
                'canara_balance': 0.00,
            },
            'pfBalance': 0.00,
            'foodcardBalance': 0.00,
        },
        'liabilities': {
            'loans': {
                'amount_paid': 0.00,
                'amount_to_pay': 0.00,
            },
            'credit_card_statement': 0.00,
            'income_tax': {
                'tax_for_FY': 0.00,
                'amount_paid': 0.00,
                'amount_to_pay': 0.00,
            }
        },
        'headlines': {
            'networth': 0.00,
            'total_assets': 0.00,
            'liquid_assets': 0.00,
            'fixed_assets': 0.00,
            'total_liability': 0.00,
        }
    }

    data = HomePageModel.objects.get(_id=ObjectId('60f92d5fac57d496f70f2361'))
    serializer = HomePageSerializer(data)
    res['assets']['bankAccounts']['icici_balance'] = float(
        serializer.data['icici_balance'])
    res['assets']['bankAccounts']['hdfc_balance'] = float(
        serializer.data['hdfc_balance'])
    res['assets']['bankAccounts']['iob_balance'] = float(
        serializer.data['iob_balance'])
    res['assets']['bankAccounts']['canara_balance'] = float(
        serializer.data['canara_balance'])
    res['assets']['pfBalance'] = float(getPFBalanceAndTxns()['balance'])
    res['assets']['foodcardBalance'] = float(
        serializer.data['foodCardBalance'])

    loan_amount_paid_so_far, loan_amounts = getLoanAmounts()
    res['liabilities']['loans']['amount_paid'] = float(loan_amount_paid_so_far)
    res['liabilities']['loans']['amount_to_pay'] = float(
        loan_amounts['amount_remaining'])
    # let the credit card txns come from the actual view - cuz the logic is complicated
    # will find workaround later
    income_tax = getTaxes()
    res['liabilities']['income_tax']['tax_for_FY'] = float(
        income_tax['tax_for_FY'])
    res['liabilities']['income_tax']['amount_paid'] = float(
        income_tax['tax_paid_so_far'])
    res['liabilities']['income_tax']['amount_to_pay'] = float(
        income_tax['remaining_tax'])
    res['liabilities']['credit_card_statement'] = creditCardData()

    res['headlines']['liquid_assets'] += res['assets']['bankAccounts']['icici_balance']
    res['headlines']['liquid_assets'] += res['assets']['bankAccounts']['hdfc_balance']
    res['headlines']['liquid_assets'] += res['assets']['bankAccounts']['iob_balance']
    res['headlines']['liquid_assets'] += res['assets']['bankAccounts']['canara_balance']
    res['headlines']['fixed_assets'] += res['assets']['pfBalance']
    res['headlines']['fixed_assets'] += res['assets']['foodcardBalance']
    res['headlines']['total_assets'] = res['headlines']['liquid_assets'] + \
        res['headlines']['fixed_assets']
    res['headlines']['total_liability'] = res['liabilities']['loans']['amount_to_pay'] + \
        res['liabilities']['income_tax']['amount_to_pay'] + \
        res['liabilities']['credit_card_statement']

    res['headlines']['networth'] = res['headlines']['total_assets'] - \
        res['headlines']['total_liability']
    print(res)
    return Response(res, status=status.HTTP_200_OK)


def creditCardData():
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

    return calculate_bill(serializer.data)['amount']
