#!/bin/bash
set -e

echo "🔄 Attente de la base de données..."
# Attendre que MySQL soit prêt
sleep 10

echo "🚀 Initialisation de la base de données..."
python init_db.py

echo "✅ Lancement de l'API FastAPI..."
exec fastapi run app/main.py --port 80
