from django.urls import path
from api import views


urlpatterns = [
    # path('networth/', views.returnNetWorth),
    # path('foodcard/', views.getFoodCardDetails),
    path('networth/', views.getTodos),
    path('foodcardbalance/', views.getfoodCardBalance)
]
