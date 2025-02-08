from django.urls import path
from . import views
from .views import transaction_chart, TransactionListView, DashboardView


app_name = 'finance'

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('create/', views.TransactionCreate.as_view(), name='transaction_create'),
    path('<int:pk>/update/', views.TransactionUpdate.as_view(), name='transaction_update'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),  # Removidos os parênteses

    path('chart/', transaction_chart, name='transaction_chart'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

