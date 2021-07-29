from django.urls import path
from bankacc import views

urlpatterns = [
    path('getalltxns/<str:bank>', views.getBankAccTxns),
    path('createtxn/<str:bank>', views.createNewTxnEntry),
    path('edittxn/<str:bank>', views.editTxn),
    path('deltxn/<str:bank>', views.deleteTxn),
]
