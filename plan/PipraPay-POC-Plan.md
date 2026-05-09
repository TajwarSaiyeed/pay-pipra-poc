# PipraPay POC - Project Plan

## Overview

A simple Proof of Concept integrating **PipraPay** (self-hosted payment automation) with a **Django** application serving both backend API and frontend templates, using **PostgreSQL** and local payment gateways (bKash, Nagad).

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend + Frontend | **Django** | Business logic, API, and templates |
| Database | **PostgreSQL** | Orders, transactions, users |
| Payments | **PipraPay** (self-hosted) | bKash / Nagad gateway integration |
| Frontend UI | Django Templates + HTMX | Simple, fast page interactions |

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   Browser   │────▶│   Django    │────▶│  PipraPay Server │
│  (Django)   │◀────│   Backend   │◀────│  (bKash/Nagad)   │
└─────────────┘     └─────────────┘     └─────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ PostgreSQL  │
                    └─────────────┘
```

### PipraPay Flow

1. Django creates a payment request via **PipraPay REST API**
2. PipraPay returns a **payment URL** (bKash/Nagad checkout)
3. User is redirected to PipraPay payment page
4. After payment, PipraPay calls Django **webhook** to confirm
5. Django updates order status to `paid`
6. User is redirected back to Django success page

---

## Project Structure

```
pay-pipra-poc/
├── config.yaml              # All configuration (DB, PipraPay credentials)
├── manage.py
├── requirements.txt
├── PipraPayPOC/
│   ├── __init__.py
│   ├── settings.py          # Loads from config.yaml
│   ├── urls.py
│   └── wsgi.py
├── orders/
│   ├── __init__.py
│   ├── models.py            # Order, Transaction
│   ├── views.py             # Checkout, webhook, dashboard
│   ├── urls.py
│   ├── services/
│   │   └── piprapay.py      # PipraPay API client
│   ├── templates/
│   │   ├── orders/
│   │   │   ├── checkout.html
│   │   │   ├── success.html
│   │   │   └── failed.html
│   │   └── dashboard.html
│   ├── admin.py
│   └── tests.py
├── docker-compose.yml       # PostgreSQL + Django
└── README.md
```

---

## Core Features

### 1. Checkout Page (`/checkout/`)
- Form: amount input, select gateway (bKash/Nagad)
- POST to Django → calls PipraPay API → redirect to payment URL

### 2. Payment Gateway Integration
- Call PipraPay `/api/v1/payment/create` to initiate payment
- Store `transaction_id`, `order_id` in PostgreSQL
- Redirect user to PipraPay payment page

### 3. Webhook Handler (`/webhook/piprapay/`)
- PipraPay POSTs payment confirmation
- Validate signature, update order status
- Return `200 OK`

### 4. Success/Fail Pages
- `/orders/success/` - Payment confirmed
- `/orders/failed/` - Payment failed/cancelled

### 5. Admin Dashboard (`/admin/`)
- View all orders with status
- Django admin panel

---

## PipraPay API Integration

### Authentication
- API Key from PipraPay admin panel
- Header: `Authorization: Bearer <API_KEY>`

### Create Payment
```http
POST /api/v1/payment/create
{
  "amount": 100,
  "currency": "BDT",
  "gateway": "bkash" | "nagad",
  "order_id": "ORD-123",
  "redirect_url": "http://localhost:8000/orders/success/",
  "Webhook_url": "http://localhost:8000/webhook/piprapay/"
}
```

### Verify Payment (via webhook or manual)
```http
GET /api/v1/payment/status/{transaction_id}
```

---

## Configuration (config.yaml)

```yaml
database:
  host: "localhost"
  port: 5432
  name: "piprapay_poc"
  user: "postgres"
  password: "postgres"

piprapay:
  base_url: "http://localhost:8080"  # PipraPay server URL
  api_key: "your-api-key"
  webhook_secret: "your-webhook-secret"

app:
  host: "0.0.0.0"
  port: 8000
  debug: true
  secret_key: "change-me-in-production"
```

---

## Implementation Steps

- [ ] **Step 1: Setup** - Docker compose, Django project, config.yaml loader
- [ ] **Step 2: PipraPay Client** - Python service to call PipraPay API
- [ ] **Step 3: Models** - Order, Transaction models
- [ ] **Step 4: Checkout Flow** - Create order → call PipraPay → redirect
- [ ] **Step 5: Webhook Handler** - Receive and process PipraPay callbacks
- [ ] **Step 6: Templates** - Checkout, success, failed pages
- [ ] **Step 7: Dashboard** - Admin panel + simple order list
- [ ] **Step 8: Testing** - Mock PipraPay for dev, or use self-hosted

---

## Notes

- PipraPay is self-hosted PHP software. You'll need a separate server/VM to install it.
- For local development without PipraPay, we can mock the API responses.
- bKash/Nagad require merchant accounts from those respective services.
