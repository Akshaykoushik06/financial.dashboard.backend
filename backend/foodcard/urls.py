from django.urls import path
from foodcard import views

urlpatterns = [
    path('getalltxns/', views.getAllFoodCardTransactions),
    path('gettxnbyid/<str:id>', views.getTxnById),
    path('edittxn/', views.editTxn),
    path('createtxn/', views.createNewTxn),
    path('deletetxn/', views.deleteTxn)
]
