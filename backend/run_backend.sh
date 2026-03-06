#!/bin/bash
set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== iniciando Backend TPV Verifactu ===${NC}"

# Install dependencies
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install -r requirements.txt

# Generate master key if missing (for testing)
if [ ! -f master.key ]; then
    echo -e "${YELLOW}Generando master key para testing...${NC}"
    python3 << 'EOF'
from cryptography.fernet import Fernet
key = Fernet.generate_key().decode()
print(f"Generated key: {key}")
with open('master.key', 'w') as f:
    f.write(key)
print("Master key saved to master.key")
EOF
else
    echo -e "${GREEN}Master key found${NC}"
fi

# Create dummy dongle file for simulation
if [ ! -f dongle.key ]; then
    echo -e "${YELLOW}Creando archivo de dongle para simulación...${NC}"
    echo "FREDO-SECURE-DONGLE-12345" > dongle.key
    echo -e "${GREEN}Dongle simulado creado${NC}"
fi

# Generate license if missing (for testing)
if [ ! -f license.key ]; then
    echo -e "${YELLOW}Generando licencia de prueba...${NC}"
    python3 << 'EOF'
from cryptography.fernet import Fernet
import json
from datetime import datetime, timedelta
import os

try:
    with open('master.key', 'rb') as f:
        key = f.read().strip()
    
    f = Fernet(key)
    license_data = {
        'dongle_id': 'FREDO-SECURE-DONGLE-12345',
        'expiracion': (datetime.now() + timedelta(days=365)).isoformat()
    }
    encrypted = f.encrypt(json.dumps(license_data).encode())
    with open('license.key', 'wb') as lf:
        lf.write(encrypted)
    print("License created successfully")
except Exception as e:
    print(f"Error creating license: {e}")
    exit(1)
EOF
else
    echo -e "${GREEN}License file found${NC}"
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creando .env desde .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Por favor, edita .env con tu configuración${NC}"
fi

# Create necessary directories
mkdir -p /tmp/verifactu_records
mkdir -p licenses

echo -e "${GREEN}Iniciando aplicación...${NC}"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

