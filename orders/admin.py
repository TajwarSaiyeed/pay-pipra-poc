from django.contrib import admin
from .models import Order, Transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'currency', 'status', 'gateway', 'transaction_id', 'created_at']
    list_filter = ['status', 'gateway', 'currency']
    search_fields = ['id', 'transaction_id']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['transaction_id', 'order__id']
    readonly_fields = ['created_at', 'updated_at']
