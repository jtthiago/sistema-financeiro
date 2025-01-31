from django.db import models

# Create your models here.

class Transaction(models.Model):
    # Define os tipos de transação possíveis (receita ou despesa)
    TRANSACTION_TYPES = (
        ('income', 'Receita'),
        ('expense', 'Despesa'),

    )
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, default="Sem descrição")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Retorna uma string representando o título e o tipo da transação
    def __str__(self):
        return f"{self.title} - {self.transaction_type.capitalize()}"
    



