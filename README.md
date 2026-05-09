# PipraPay POC

A Django app integrating **PipraPay** (self-hosted payment automation) with **bKash** and **Nagad** gateways.

---

## Quick Start (1 Command)

```bash
git pull origin main && bash start.sh
```

Then:
1. Get API key from **https://demo.piprapay.com/admin/** (login: `demo` / `12345678`)
2. Copy the API key from **Settings → API Keys**
3. Update `config.yaml` with your API key
4. Restart the server

---

## URLs

| Page | URL |
|---|---|
| Checkout | `http://localhost:8000/checkout/` |
| Admin | `http://localhost:8000/admin/` |
| Success | `http://localhost:8000/orders/success/` |
| Failed | `http://localhost:8000/orders/failed/` |
| Webhook | `http://localhost:8000/webhook/piprapay/` |

---

## Setup

### 1. Get PipraPay API Key

1. Go to **https://demo.piprapay.com/admin/**
2. Login: `demo` / `12345678`
3. Go to **Settings → API Keys**
4. Copy the API key

### 2. Update config.yaml

```bash
nano config.yaml
```

Update the `api_key`:

```yaml
piprapay:
  api_key: "YOUR-API-KEY-HERE"
```

### 3. Restart

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## Payment Flow

1. User submits checkout form (amount + gateway)
2. Django creates Order in SQLite DB
3. Django calls PipraPay API
4. User redirected to bKash/Nagad page
5. PipraPay calls webhook on Django
6. Django updates order status
7. User redirected to success page

---

## Project Structure

```
├── config.yaml              # Configuration (DB, PipraPay)
├── requirements.txt
├── manage.py
├── start.sh                # Run everything with 1 command
├── Dockerfile
├── docker-compose.yml
├── PipraPayPOC/             # Django project
├── orders/                  # Main app
│   ├── models.py            # Order, Transaction
│   ├── views.py             # Checkout, webhook
│   └── services/
│       └── piprapay.py      # PipraPay API client
└── piprapay/               # PipraPay source (for self-hosting)
```
