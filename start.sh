#!/bin/bash

echo "======================================"
echo " PipraPay POC - Setup Script"
echo "======================================"
echo ""

# Step 1: Install Python dependencies
echo "[1/3] Installing Python dependencies..."
pip install -r requirements.txt -q

# Step 2: Create & run migrations
echo "[2/3] Running migrations..."
python manage.py makemigrations orders 2>/dev/null
python manage.py migrate

# Step 3: Start Django
echo "[3/3] Starting Django..."
echo ""
echo "======================================"
echo " Django: http://localhost:8000"
echo " Checkout: http://localhost:8000/checkout/"
echo " Admin: http://localhost:8000/admin/"
echo "======================================"
echo ""

python manage.py runserver 0.0.0.0:8000
