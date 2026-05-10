import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class PipraPayClient:
    def __init__(self):
        self.base_url = settings.PIPRAPAY_BASE_URL
        self.api_key = settings.PIPRAPAY_API_KEY
        self.webhook_secret = settings.PIPRAPAY_WEBHOOK_SECRET

    def _headers(self):
        return {
            'MHS-PIPRAPAY-API-KEY': self.api_key,
            'Content-Type': 'application/json',
        }

    def create_payment(self, order_id: str, amount: float, gateway: str,
                       redirect_url: str, webhook_url: str, currency: str = 'BDT',
                       full_name: str = '', email: str = '', mobile: str = ''):
        payload = {
            'full_name': full_name or str(order_id),
            'email_address': email or '',
            'mobile_number': mobile or '',
            'amount': amount,
            'currency': currency,
            'gateway': gateway,
            'return_url': redirect_url,
            'webhook_url': webhook_url,
        }

        url = f'{self.base_url}/api/checkout/redirect'
        logger.info(f"[PipraPay] Creating payment: {payload}")

        try:
            response = requests.post(url, json=payload, headers=self._headers(), timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"[PipraPay] Response: {data}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"[PipraPay] Error: {e}")
            raise

    def get_payment_status(self, transaction_id: str):
        url = f'{self.base_url}/api/v1/payment/status/{transaction_id}'

        try:
            response = requests.get(url, headers=self._headers(), timeout=30)
            logger.error(f"[PipraPay] Response body: {response.text}")  
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"[PipraPay] Error: {e}")
            raise


piprapay_client = PipraPayClient()
