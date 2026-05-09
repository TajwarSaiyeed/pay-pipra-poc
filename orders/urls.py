from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/pay/', views.create_order_and_pay, name='create_order_and_pay'),
    path('orders/success/', views.success_view, name='success'),
    path('orders/failed/', views.failed_view, name='failed'),
    path('webhook/piprapay/', views.webhook_view, name='webhook'),
]
