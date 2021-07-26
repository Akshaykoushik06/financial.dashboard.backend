from django.urls import path
from creditcard import views

urlpatterns = [
    path('gettxns/', views.getCreditCardTxns),
    path('createtxn/', views.createTxnEntry),
    path('edittxn/', views.editTxnEntry),
    path('deletetxn/', views.deleteTxnEntry),
]
