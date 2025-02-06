from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.dateparse import parse_date
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
    # Obtendo transações, agrupando por mês e tipo
    transactions = Transaction.objects.annotate(month=TruncMonth('date')).values('month', 'transaction_type') \
                .annotate(total=Sum('amount')).order_by('month')
    
    # Inicializando listas para despesas e receitas
    income_months = [0] * 12  # 12 meses
    expense_months = [0] * 12  # 12 meses

    # Preenchendo os valores de receita e despesa para cada mês
    for transaction in transactions:
        month = transaction['month'].month - 1  # mês em Django é 1-indexed, ajustamos para 0-indexed
        if transaction['transaction_type'] == 'income':
            income_months[month] = transaction['total']
        elif transaction['transaction_type'] == 'expense':
            expense_months[month] = transaction['total']

    # Meses do ano
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Configurando o gráfico
    ax.bar(months, expense_months, color='red', width=0.4, label='Despesas', align='center')
    ax.bar(months, income_months, color='green', width=0.4, label='Receitas', align='edge')

    # Personalizando o gráfico
    ax.set_ylabel('Total R$')
    ax.set_xlabel('Meses')
    ax.set_title('Receitas e Despesas por Mês')
    ax.legend()

    # Salvando a imagem na memória
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)  # Fecha o gráfico para evitar consumo excessivo de memória

    # Retorna a imagem gerada como resposta HTTP
    return HttpResponse(buffer.getvalue(), content_type='image/png')

class TransactionListView(ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        search_query = self.request.GET.get('q')

        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(date__gte=start_date)
        
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(date__lte=end_date)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |  
                Q(description__icontains=search_query)
            )

    

        return queryset

        