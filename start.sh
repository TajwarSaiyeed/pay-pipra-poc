#!/bin/bash

echo ">>> Installing dependencies..."
pip install -r requirements.txt -q

echo ">>> Creating migrations..."
python manage.py makemigrations orders

echo ">>> Running migrations..."
python manage.py migrate

echo ">>> Starting server..."
echo ""
echo ">>> Django running at http://localhost:8000"
echo ">>> Checkout: http://localhost:8000/checkout/"
echo ">>> Admin: http://localhost:8000/admin/"
echo ""
echo ">>> GET YOUR API KEY FROM:"
echo ">>> https://demo.piprapay.com/admin/"
echo ">>> Login: demo / 12345678"
echo ">>> Then update config.yaml with your API key"
echo ""
python manage.py runserver 0.0.0.0:8000
