# PipraPay POC

A Django app integrating **PipraPay** (self-hosted payment automation) with **bKash** and **Nagad** gateways. Everything runs on GitHub Codespaces (or any VPS).

---

## Quick Start

```bash
git pull origin main && bash start.sh
```

---

## Setup PipraPay (Self-Hosted)

### Option 1: Docker (Recommended for Codespaces with Docker enabled)

1. Go to **https://github.com/settings/codespaces**
2. Click **Edit** on your codespace
3. Enable **Docker in Codespaces**
4. Recreate the codespace

Then run `bash start.sh` — it will auto-start PipraPay container.

### Option 2: Manual VPS Setup

If running on your own VPS with root access:

```bash
# Install requirements
sudo apt-get update
sudo apt-get install -y apache2 php php-mysql php-curl php-xml php-mbstring

# Clone/setup PipraPay
cd /var/www/
sudo git clone https://github.com/PipraPay/PipraPay.git piprapay
sudo chown -R www-data:www-data /var/www/piprapay

# Configure Apache (point to piprapay directory)
# Then access at http://YOUR-VPS-IP:8080
```

---

## Configuration

After PipraPay is running, get your API key:

1. Go to **http://YOUR-PIPRAPAY-SERVER:8080/admin/**
2. Login and go to **Settings → API Keys**
3. Copy the API key

Update `config.yaml`:

```yaml
piprapay:
  base_url: "http://YOUR-PIPRAPAY-SERVER:8080"
  api_key: "YOUR-API-KEY-HERE"
```

---

## URLs

| Page | URL |
|---|---|
| Django App | `http://localhost:8000` |
| Checkout | `http://localhost:8000/checkout/` |
| Django Admin | `http://localhost:8000/admin/` |
| PipraPay Admin | `http://localhost:8080` |

---

## Payment Flow

1. User submits checkout form (amount + gateway)
2. Django creates Order in SQLite DB
3. Django calls PipraPay API (`/api/v1/payment/create`)
4. PipraPay returns payment URL (bKash/Nagad)
5. User redirected to complete payment
6. PipraPay calls `/webhook/piprapay/` on Django
7. Django updates order status
8. User redirected to success page

---

## Project Structure

```
├── config.yaml              # All configuration
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
└── piprapay/               # PipraPay source
```

---

## Notes

- **bKash/Nagad** require separate merchant accounts
- PipraPay core is encrypted (IonCube), but plugins/themes are open-source
- For local testing without real payments, use the demo server at `https://demo.piprapay.com`
