#!/bin/bash

echo "======================================"
echo " PipraPay POC - Full Setup Script"
echo "======================================"
echo ""

# Step 1: Install Python dependencies
echo "[1/4] Installing Python dependencies..."
pip install -r requirements.txt -q

# Step 2: Create & run migrations
echo "[2/4] Running migrations..."
python manage.py makemigrations orders 2>/dev/null
python manage.py migrate

# Step 3: Build & Start PipraPay
echo "[3/4] Building PipraPay container..."
cd piprapay
/usr/bin/docker build -t piprapay . && /usr/bin/docker rm -f piprapay 2>/dev/null && /usr/bin/docker run -d -p 8080:80 --name piprapay piprapay
cd ..

# Step 4: Start Django
echo "[4/4] Starting Django..."
echo ""
echo "======================================"
echo " Django: http://localhost:8000"
echo " PipraPay: http://localhost:8080"
echo " Checkout: http://localhost:8000/checkout/"
echo "======================================"
echo ""
echo ">>> Next steps:"
echo ">>> 1. Open http://localhost:8080 -> PipraPay install wizard"
echo ">>> 2. Complete PipraPay setup"
echo ">>> 3. Settings -> API Keys -> copy key"
echo ">>> 4. Update config.yaml with API key"
echo ">>> 5. Restart Django: python manage.py runserver 0.0.0.0:8000"
echo ""

python manage.py runserver 0.0.0.0:8000
