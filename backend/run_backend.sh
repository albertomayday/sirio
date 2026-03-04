#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Generate keys if missing (for testing)
if [ ! -f master.key ]; then
    python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > master.key
fi

if [ ! -f license.key ]; then
    # Create a dummy license
    python3 -c "
from cryptography.fernet import Fernet
import json
from datetime import datetime, timedelta
import os

key = open('master.key', 'rb').read().strip()
f = Fernet(key)
license_data = {
    'dongle_id': 'FREDO-SECURE-DONGLE-12345',
    'expiracion': (datetime.now() + timedelta(days=365)).isoformat()
}
encrypted = f.encrypt(json.dumps(license_data).encode())
with open('license.key', 'wb') as lf:
    lf.write(encrypted)
"
fi

# Create dummy dongle file for simulation
echo "FREDO-SECURE-DONGLE-12345" > dongle.key

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
