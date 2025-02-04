from django.contrib import admin
from .models import Transaction

# Register your models here.


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'transaction_type', 'date')
    list_filter = ('transaction_type',)
    search_fields = ('title',)


