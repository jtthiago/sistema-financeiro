from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from .models import Transaction
from django.urls import reverse_lazy
import matplotlib.pyplot as plt
from django.http import HttpResponse
from io import BytesIO
import matplotlib

matplotlib.use('Agg')



class TransactionList(ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'

class TransactionCreate(CreateView):
    model = Transaction
    fields = ['title','description', 'amount', 'transaction_type', 'date']
    template_name = 'finance/transaction_form.html'
    success_url = '/finance/'

class TransactionUpdate(UpdateView):
    model = Transaction
    fields = ['title','description', 'amount', 'transaction_type', 'date']
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('finance:transaction_list')

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    messages.success(request, "Transação excluída com sucesso!")
    return redirect('finance:transaction_list')


def transaction_chart(request):
    # Obtendo dados das transações
    transactions = Transaction.objects.all()

    # Contabilizando valores por tipo de transação
    income_total = sum(t.amount for t in transactions if t.transaction_type == "income")
    expense_total = sum(t.amount for t in transactions if t.transaction_type == "expense")

    # Criando os rótulos e valores
    labels = ["Receitas", "Despesas"]
    values = [income_total, expense_total]

    # Criando o gráfico
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['blue', 'red'])

    # Personalizando o gráfico
    ax.set_ylabel('Total R$')
    ax.set_xlabel('Tipo de Transação')
    ax.set_title('Receitas vs Despesas')
    plt.xticks(rotation=0)

    # Salvando a imagem na memória
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)  # Fecha o gráfico para evitar consumo excessivo de memória

    return HttpResponse(buffer.getvalue(), content_type='image/png')