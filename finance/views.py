from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Transaction
from django.urls import reverse_lazy


class TransactionList(ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'

class TransactionCreate(CreateView):
    model = Transaction
    fields = ['description', 'amount', 'category', 'date']
    template_name = 'finance/transaction_form.html'
    success_url = '/finance/'

class TransactionUpdate(UpdateView):
    model = Transaction
    fields = ['description', 'amount', 'category', 'date']
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('finance:transaction_list')

class TransactionDelete(DeleteView):
    model = Transaction
    template_name = 'finance/transaction_confirm_delete.html'
    success_url = reverse_lazy('finance:transaction_list')
