from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from .models import Transaction
from django.urls import reverse_lazy


class TransactionList(ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'

class TransactionCreate(CreateView):
    model = Transaction
    fields = ['title','description', 'amount', 'transaction_type', 'category', 'date']
    template_name = 'finance/transaction_form.html'
    success_url = '/finance/'

class TransactionUpdate(UpdateView):
    model = Transaction
    fields = ['title','description', 'amount', 'transaction types', 'category', 'date']
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('finance:transaction_list')

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    messages.success(request, "Transação excluída com sucesso!")
    return redirect('finance:transaction_list')