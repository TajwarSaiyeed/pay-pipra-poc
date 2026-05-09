# PipraPay POC

A Django proof-of-concept integrating **PipraPay** (self-hosted payment automation) with **bKash** and **Nagad** gateways.

---

## Quick Start (GitHub Codespaces)

1. Click **Code** → **Codespaces** → **Create codespace**
2. Wait for the container to build
3. App runs at `https://<your-codespace>.app.github.dev:8000`
4. Run migrations: `python manage.py migrate`
5. Create admin: `python manage.py createsuperuser`
6. Visit `/checkout/` to test payments

---

## Local Development

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

- App: `http://localhost:8000/checkout/`
- Admin: `http://localhost:8000/admin/`

---

## Setup

### 1. Get PipraPay running

You need a **running PipraPay server**. Options:

- **Demo**: `https://demo.piprapay.com` (login: `demo` / `12345678`)
- **Self-hosted**: Download from [piprapay.com/download](https://piprapay.com/download)

### 2. Update config.yaml

```yaml
piprapay:
  base_url: "https://your-piprapay-domain.com"
  api_key: "your-piprapay-api-key"
  webhook_secret: "your-webhook-secret"
```

Get API key from PipraPay admin → Settings → API Keys

### 3. Install plugins

In PipraPay admin, install and configure **bKash** and **Nagad** plugins.

---

## Important: Webhook Setup

For real payment webhooks to work, your Django app needs a **public URL**.

**GitHub Codespaces:**
- Use the Codespaces preview URL (e.g., `https://greatest-1234a-5678b9c0d1234e567.preview.app.github.dev:8000`)
- Update `allowed_hosts` in `config.yaml` to include your codespace domain
- For testing, you can skip webhooks and verify orders manually in admin

**Local Development:**
- Use [ngrok](https://ngrok.com): `ngrok http 8000`
- Update redirect_url and webhook_url to ngrok URL

---

## Project Structure

```
├── config.yaml              # All configuration
├── requirements.txt
├── manage.py
├── Dockerfile
├── docker-compose.yml       # PostgreSQL + Django
├── PipraPayPOC/             # Django project
│   ├── settings.py          # Loads from config.yaml
│   └── urls.py
├── orders/                  # Main app
│   ├── models.py            # Order, Transaction
│   ├── views.py            # Checkout, webhook
│   └── services/
│       └── piprapay.py     # PipraPay API client
└── templates/
    ├── checkout.html
    ├── success.html
    └── failed.html
```

---

## Payment Flow

1. User submits checkout form
2. Django creates Order in PostgreSQL
3. Django calls PipraPay `/api/v1/payment/create`
4. PipraPay returns payment URL (bKash/Nagad page)
5. User redirected to complete payment
6. PipraPay calls `/webhook/piprapay/` on Django
7. Django updates order status to `paid`
8. User redirected to success page

---

## URLs

| Page | URL |
|---|---|
| Checkout | `/checkout/` |
| Success | `/orders/success/` |
| Failed | `/orders/failed/` |
| Webhook | `/webhook/piprapay/` |
| Admin | `/admin/` |

---

## Notes

- bKash/Nagad require separate merchant accounts
- For testing without real payments, you can enable `mock_mode: true` in config.yaml
- All config is in `config.yaml` — no hardcoding
