from django.urls import path
from api import views


urlpatterns = [
    path('homepage/', views.returnHomePageData),
    # path('foodcard/', views.getFoodCardDetails),
    # path('networth/', views.getTodos),
    path('foodcardbalance/', views.getfoodCardBalance)
]
