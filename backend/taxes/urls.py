from django.urls import path
from taxes import views

urlpatterns = [
    path('getalltxns/', views.getAllTxns),
    path('createtxn/', views.createTxn),
    path('edittxn/', views.editTxn),
    path('deltxn/', views.delTxn),
]
