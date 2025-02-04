from django.urls import path
from . import views
from .views import transaction_chart

app_name = 'finance'

urlpatterns = [
    path('', views.TransactionList.as_view(), name='transaction_list'),
    path('create/', views.TransactionCreate.as_view(), name='transaction_create'),
    path('<int:pk>/update/', views.TransactionUpdate.as_view(), name='transaction_update'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),  # Removidos os parênteses

    path('chart/', transaction_chart, name='transaction_chart'),
]

