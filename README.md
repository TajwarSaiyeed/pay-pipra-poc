# PipraPay POC

A Django proof-of-concept integrating **PipraPay** (self-hosted) with **bKash** and **Nagad** gateways.

---

## Quick Start

### Without Docker (SQLite - recommended for Codespaces)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### With Docker (PostgreSQL)

```bash
cp config.yaml.docker config.yaml
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Ports

| Service | Port | URL |
|---|---|---|
| Django App | 8000 | `/checkout/` |
| PipraPay Admin | 8080 | `/admin/` |
| PostgreSQL | 5432 | (internal) |

---

## Setup PipraPay

1. Start PipraPay at port 8080:
   ```bash
   cd piprapay
   docker build -t piprapay .
   docker run -d -p 8080:80 --name piprapay piprapay
   ```
2. Go to `http://localhost:8080` → complete install wizard
3. Settings → API Keys → copy key → paste in `config.yaml`
4. Install bKash/Nagad plugins in PipraPay admin

---

## Payment Flow

1. User submits checkout form
2. Django creates Order in DB
3. Django calls PipraPay `/api/v1/payment/create`
4. User redirected to bKash/Nagad page
5. PipraPay calls `/webhook/piprapay/` on Django
6. Django updates order status to `paid`
7. User redirected to success page

---

## Project Structure

```
├── config.yaml              # SQLite config (local)
├── config.yaml.docker       # PostgreSQL config (Docker)
├── requirements.txt
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── PipraPayPOC/
│   ├── settings.py         # Auto-detects SQLite or PostgreSQL
│   └── urls.py
├── orders/
│   ├── models.py           # Order, Transaction
│   ├── views.py           # Checkout, webhook
│   └── services/
│       └── piprapay.py     # PipraPay API client
└── piprapay/              # PipraPay source
```
