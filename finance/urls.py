from django.urls import path
from . import views


app_name = 'finance'

urlpatterns = [
    path('', views.TransactionList.as_view(), name='transaction_list'),
    path('create/', views.TransactionCreate.as_view(), name='transation_create'),
    path('<int:pk>/update/', views.TransactionUpdate.as_view(), name='transaction_update'),
    path('<int:pk>/delete/', views.TransactionDelete.as_view(), name='transaction_delete'),
]

