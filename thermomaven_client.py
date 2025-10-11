import requests
import json
import hashlib
import time
import uuid
import random
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class ThermoMavenClient:
    def __init__(self, email, password):
        self.base_url = "https://api.iot.thermomaven.de"
        self.email = email
        self.password = password
        self.token = None
        self.device_sn = ''.join(random.choices('0123456789abcdef', k=16))
        self.app_id = "thermomavencom"  # Project ID trouvé
        self.app_key = ""  # AppKey à trouver
    
    def _generate_sign(self, params_str, body_str=""):
        # Format: appKey|params_str|body_str (sans le dernier | si pas de body)
        sign_str = self.app_key + "|" + params_str
        if body_str:
            sign_str += "|" + body_str
        # Supprimer les newlines comme dans le code original
        sign_str = sign_str.replace('\n', '')
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    
    def _build_headers(self, body=None):
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4()).replace("-", "").lower()
        
        params = {
            "x-appId": self.app_id,
            "x-appVersion": "1804",
            "x-deviceSn": self.device_sn,
            "x-lang": "en_US",
            "x-nonce": nonce,
            "x-timestamp": timestamp,
            "x-token": self.token if self.token else "",
        }
        
        # Trier les paramètres et créer la chaîne sans ; à la fin
        params_sorted = sorted(params.items())
        params_str = ";".join([f"{k}={v}" for k, v in params_sorted])
        body_str = json.dumps(body, separators=(',', ':')) if body else ""
        sign = self._generate_sign(params_str, body_str)
        
        headers = params.copy()
        headers["x-sign"] = sign
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "okhttp/4.12.0"
        
        return headers
    
    def login(self):
        endpoint = f"{self.base_url}/app/account/login"
        payload = {"email": self.email, "password": self.password}
        headers = self._build_headers(payload)
        
        print("=== LOGIN ===")
        print("AppId:", self.app_id)
        print("DeviceSn:", self.device_sn)
        print("AppKey:", self.app_key if self.app_key else "(empty)")
        
        # Debug: montrer la signature
        params_sorted = sorted([k for k in headers.keys() if k.startswith("x-") and k != "x-sign"])
        params_str = ";".join([f"{k}={headers[k]}" for k in params_sorted])
        body_str = json.dumps(payload, separators=(',', ':'))
        sign_input = f"{self.app_key}|{params_str}|{body_str}"
        print("Sign input:", sign_input[:100], "..." if len(sign_input) > 100 else "")
        print("x-sign:", headers.get("x-sign"))
        
        response = requests.post(endpoint, json=payload, headers=headers)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {response.text}\n")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "0":
                self.token = data.get("data", {}).get("token")
                print("[OK] Login successful!")
                return data
            else:
                print(f"[ERROR] {data.get('msg')}")
        return None
    
if __name__ == "__main__":
    print("Starting ThermoMaven Client...")
    
    # Récupérer les identifiants depuis les variables d'environnement
    email = os.getenv('THERMOMAVEN_EMAIL')
    password = os.getenv('THERMOMAVEN_PASSWORD')
    app_key = os.getenv('THERMOMAVEN_APP_KEY', '')
    
    if not email or not password:
        print("[ERROR] Please set THERMOMAVEN_EMAIL and THERMOMAVEN_PASSWORD environment variables")
        print("Create a .env file with:")
        print("THERMOMAVEN_EMAIL=your-email@example.com")
        print("THERMOMAVEN_PASSWORD=your-password")
        print("THERMOMAVEN_APP_KEY=your-app-key")
        exit(1)
    
    client = ThermoMavenClient(email, password)
    client.app_key = app_key
    result = client.login()
    
    if result:
        print("\n=== SUCCESS ===")
    else:
        print("\n=== FAILED ===")