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
            full_name = request.POST.get('full_name', f'Customer-{uuid.uuid4().hex[:8]}')
            email = request.POST.get('email', '')
            mobile = request.POST.get('mobile', '')

            if amount <= 0:
                return render(request, 'orders/checkout.html', {
                    'error': 'Amount must be greater than 0'
                })

            order = Order.objects.create(
                amount=amount,
                currency='BDT',
                gateway=gateway,
            )

            public_host = 'special-space-fiesta-q5rr695pq9xcr6v-8000.app.github.dev'
            redirect_url = f"https://{public_host}/orders/success/?order_id={order.id}"
            webhook_url = f"https://{public_host}/webhook/piprapay/"

            try:
                email = request.POST.get('email', '')
                if not email or '@' not in email:
                    email = f'customer-{order.id}@example.com'
                mobile = request.POST.get('mobile', '')
                if not mobile:
                    mobile = '01712345678'
                response = piprapay_client.create_payment(
                    order_id=str(order.id),
                    amount=amount,
                    gateway=gateway,
                    redirect_url=redirect_url,
                    webhook_url=webhook_url,
                    full_name=request.POST.get('full_name', f'Customer-{order.id}'),
                    email=email,
                    mobile=mobile,
                )

                transaction_id = response.get('pp_id', str(uuid.uuid4()))
                payment_url = response.get('pp_url', '').replace('\\/', '/')

                if payment_url.startswith('http://localhost:8080'):
                    payment_url = payment_url.replace('http://localhost:8080', 'https://special-space-fiesta-q5rr695pq9xcr6v-8080.app.github.dev')
                elif payment_url.startswith('http://piprapay/'):
                    payment_url = payment_url.replace('http://piprapay/', 'https://special-space-fiesta-q5rr695pq9xcr6v-8080.app.github.dev/')

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
