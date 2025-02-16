from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView
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

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'finance/transaction_confirm_delete.html'  # Crie esse template
    success_url = reverse_lazy('finance:transaction_list')

    def form_valid(self, form):
        messages.success(self.request, "Transação excluída com sucesso!")
        return super().form_valid(form)
        



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


@method_decorator(login_required, name='dispatch')
class TransactionListView(ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 10  # Adicionando paginação
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date')  # Mantém a ordenação padrão
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


    

class DashboardView(TemplateView):
    template_name = "finance/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filtro de data
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Filtra as transações com base no tipo e data
        transactions = Transaction.objects.all()

        if start_date:
            start_date = parse_date(start_date)
            transactions = transactions.filter(date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            transactions = transactions.filter(date__lte=end_date)

        # Cálculo de receitas e despesas
        receitas = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
        despesas = transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

        # Calcula o saldo total
        saldo_total = receitas - despesas

        context['saldo_total'] = saldo_total
        context['receitas'] = receitas
        context['despesas'] = despesas

        # Resumo mensal
        resumo_mensal = (
            transactions
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        context['resumo_mensal'] = resumo_mensal
        return context
    
class ListaTransacoesView(ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 10  # Define a paginação para 10 itens por página
    ordering = ['-date']  # Ordena por data mais recente primeiro

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date')  # Mantém a ordenação
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context