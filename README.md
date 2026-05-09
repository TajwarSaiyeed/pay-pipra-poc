# PipraPay POC

A Django proof-of-concept integrating **PipraPay** (self-hosted) with **bKash** and **Nagad** gateways. Everything runs on GitHub Codespaces.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              GitHub Codespaces              │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Django  │  │ PipraPay │  │    DB    │  │
│  │ :8000    │  │  :8080   │  │ Postgres │  │
│  └────┬─────┘  └────┬─────┘  └──────────┘  │
│       │             │                       │
│       └────────────┘                       │
│    Django calls PipraPay API               │
└─────────────────────────────────────────────┘
```

---

## Quick Start (GitHub Codespaces)

1. Push to GitHub → **Code** → **Codespaces** → **Create codespace on main**
2. Wait for Docker build to complete
3. Open terminal and run:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```
4. Visit the Ports tab → port **8000** (Django) and **8080** (PipraPay admin)

---

## Services

| Service | URL | Purpose |
|---|---|---|
| Django App | `http://localhost:8000` | Checkout, webhook handler |
| PipraPay Admin | `http://localhost:8080` | Payment gateway admin |
| PostgreSQL | `:5432` | Orders database |

---

## Setup PipraPay (First Time)

1. Open PipraPay admin at `http://localhost:8080`
2. Login with admin credentials (set during PipraPay install wizard)
3. Go to **Settings → API Keys** → Create new API key
4. Copy the API key
5. Update `config.yaml`:
   ```yaml
   piprapay:
     api_key: "your-api-key"
   ```
6. Go to **Modules** → Install and configure **bKash** and **Nagad** plugins

---

## Usage

- **Checkout**: `http://localhost:8000/checkout/`
- **PipraPay Admin**: `http://localhost:8080/admin/`
- **Django Admin**: `http://localhost:8000/admin/`

### Payment Flow

1. User submits checkout form (amount + gateway)
2. Django creates Order in PostgreSQL
3. Django calls `POST /api/v1/payment/create` on PipraPay
4. PipraPay returns payment URL (bKash/Nagad page)
5. User redirected to complete payment
6. PipraPay calls `/webhook/piprapay/` on Django
7. Django updates order status to `paid`
8. User redirected to success page

---

## Project Structure

```
├── config.yaml              # All configuration
├── requirements.txt
├── manage.py
├── Dockerfile              # Django
├── docker-compose.yml      # Django + PipraPay + PostgreSQL
├── PipraPayPOC/             # Django project
│   ├── settings.py
│   └── urls.py
├── piprapay/               # PipraPay source (cloned from GitHub)
│   └── Dockerfile
├── orders/                  # Main Django app
│   ├── models.py            # Order, Transaction
│   ├── views.py             # Checkout, webhook
│   └── services/
│       └── piprapay.py      # PipraPay API client
└── .devcontainer/
    └── devcontainer.json
```

---

## Notes

- bKash/Nagad require separate merchant accounts from those services
- For testing, you can skip webhooks and verify orders manually in Django admin
- PipraPay core is encrypted (IonCube), but plugins/themes are open-source
