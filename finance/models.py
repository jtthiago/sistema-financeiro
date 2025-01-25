from django.db import models

# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Receita'),
        ('expense', 'Despesa'),

    )

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
