import uuid
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Order, Transaction
from .services.piprapay import piprapay_client

logger = logging.getLogger(__name__)


def home(request):
    return redirect('checkout')


def checkout_view(request):
    return render(request, 'orders/checkout.html')


def create_order_and_pay(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount', 0))
            gateway = request.POST.get('gateway', '')

            if amount <= 0:
                return render(request, 'orders/checkout.html', {
                    'error': 'Amount must be greater than 0'
                })

            order = Order.objects.create(
                amount=amount,
                currency='BDT',
                gateway=gateway,
            )

            scheme = 'https' if request.is_secure() else 'http'
            host = request.get_host()
            redirect_url = f"{scheme}://{host}/orders/success/?order_id={order.id}"
            webhook_url = f"{scheme}://{host}/webhook/piprapay/"

            try:
                response = piprapay_client.create_payment(
                    order_id=str(order.id),
                    amount=amount,
                    gateway=gateway,
                    redirect_url=redirect_url,
                    webhook_url=webhook_url,
                )

                transaction_id = response.get('transaction_id', str(uuid.uuid4()))
                payment_url = response.get('payment_url', '')

                Transaction.objects.create(
                    order=order,
                    transaction_id=transaction_id,
                    status='pending',
                    gateway_response=response,
                )
                order.transaction_id = transaction_id
                order.save()

                if payment_url:
                    return redirect(payment_url)
                else:
                    return render(request, 'orders/checkout.html', {
                        'error': 'No payment URL received'
                    })

            except Exception as e:
                logger.error(f"Payment error: {e}")
                order.status = 'failed'
                order.save()
                return render(request, 'orders/checkout.html', {
                    'error': f'Failed to connect to PipraPay: {str(e)}'
                })

        except (ValueError, TypeError):
            return render(request, 'orders/checkout.html', {
                'error': 'Invalid amount'
            })

    return redirect('checkout')


def success_view(request):
    order_id = request.GET.get('order_id')
    order = None
    if order_id:
        try:
            order = get_object_or_404(Order, id=order_id)
        except Exception:
            pass
    return render(request, 'orders/success.html', {'order': order})


def failed_view(request):
    return render(request, 'orders/failed.html')


@csrf_exempt
def webhook_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        import json
        payload = json.loads(request.body)

        transaction_id = payload.get('transaction_id')
        order_id = payload.get('order_id')
        payment_status = payload.get('status')

        logger.info(f"[Webhook] Received: {payload}")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            logger.error(f"[Webhook] Order not found: {order_id}")
            return JsonResponse({'error': 'Order not found'}, status=404)

        if payment_status == 'success':
            order.status = 'paid'
            order.save()
            Transaction.objects.filter(order=order).update(
                status='success',
                gateway_response=payload,
            )
        elif payment_status == 'failed':
            order.status = 'failed'
            order.save()
            Transaction.objects.filter(order=order).update(
                status='failed',
                gateway_response=payload,
            )

        return JsonResponse({'status': 'received'})

    except Exception as e:
        logger.error(f"[Webhook] Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
