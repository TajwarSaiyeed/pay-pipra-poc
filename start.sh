#!/bin/bash

echo "======================================"
echo " PipraPay POC - Setup Script"
echo "======================================"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "[1/6] Docker detected!"
    echo "[2/6] Starting PipraPay with Docker..."
    
    # Build and run PipraPay container
    cd piprapay && docker build -t piprapay . 2>/dev/null && docker run -d -p 8080:80 --name piprapay piprapay 2>/dev/null
    cd ..
    
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo ">>> PipraPay running at http://localhost:8080"
    else
        echo ">>> WARNING: PipraPay container failed to start"
        echo ">>> You may need to enable Docker in Codespaces settings"
    fi
else
    echo "[1/6] Docker not available..."
    echo ">>> Skipping PipraPay container (use demo server for now)"
fi

# Step 2: Install Python dependencies
echo "[2/6] Installing Python dependencies..."
pip install -r requirements.txt -q

# Step 3: Create migrations
echo "[3/6] Creating migrations..."
python manage.py makemigrations orders 2>/dev/null

# Step 4: Run migrations
echo "[4/6] Running migrations..."
python manage.py migrate

# Step 5: Check config
echo "[5/6] Checking config.yaml..."

if grep "YOUR-PIPRAPAY-SERVER" config.yaml > /dev/null 2>&1; then
    echo ">>> WARNING: You need to configure config.yaml"
    echo ">>> 1. Start PipraPay at http://localhost:8080"
    echo ">>> 2. Go to PipraPay admin -> Settings -> API Keys"
    echo ">>> 3. Update config.yaml with your PipraPay server URL and API key"
fi

# Step 6: Start Django
echo "[6/6] Starting Django..."
echo ""
echo "======================================"
echo " Django: http://localhost:8000"
echo " PipraPay: http://localhost:8080 (if Docker worked)"
echo " Checkout: http://localhost:8000/checkout/"
echo " Admin: http://localhost:8000/admin/"
echo "======================================"
echo ""

python manage.py runserver 0.0.0.0:8000
