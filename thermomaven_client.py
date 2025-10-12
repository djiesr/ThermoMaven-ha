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
        self.base_url = "https://api.iot.thermomaven.com"
        self.email = email
        self.password = password
        self.token = None
        self.user_id = None
        self.device_sn = ''.join(random.choices('0123456789abcdef', k=16))
        self.app_id = ""
        self.app_key = ""
    
    def _generate_sign(self, params_str, body_str=""):
        sign_str = self.app_key + "|" + params_str
        if body_str:
            sign_str += "|" + body_str
        sign_str = sign_str.replace('\n', '')
        
        print(f"\n=== SIGNATURE DEBUG ===")
        print(f"Sign string: {sign_str}")
        md5_hash = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        print(f"MD5: {md5_hash}")
        print(f"=== END DEBUG ===\n")
        
        return md5_hash
    
    def _build_headers(self, body=None):
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4()).replace("-", "").lower()
        
        token_value = self.token if self.token else "none"
        
        params = {
            "x-appId": self.app_id,
            "x-appVersion": "1804",
            "x-deviceSn": self.device_sn,
            "x-lang": "en_US",
            "x-nonce": nonce,
            "x-region": "US",
            "x-timestamp": timestamp,
            "x-token": token_value,
        }
        
        # Trier les paramètres
        params_sorted = sorted(params.items())
        params_str = ";".join([f"{k}={v}" for k, v in params_sorted])
        
        # Body JSON - sans espaces, sans échappement Unicode
        if body:
            body_str = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
            print(f"DEBUG body_str: {body_str}")
        else:
            body_str = ""
        
        # Calculer la signature
        sign = self._generate_sign(params_str, body_str)
        
        # Ajouter x-sign aux headers
        headers = params.copy()
        headers["x-sign"] = sign
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "okhttp/4.12.0"
        
        return headers
    
    def login(self):
        endpoint = f"{self.base_url}/app/account/login"
        
        # Hash le mot de passe en MD5
        password_md5 = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        
        # Payload exact comme dans Frida
        payload = {
            "accountName": self.email,
            "accountPassword": password_md5,
            "deviceInfo": "google sdk_gphone_x86_64 11"
        }
        
        headers = self._build_headers(payload)
        
        print("=== LOGIN ===")
        print(f"AppId: {self.app_id}")
        print(f"AppKey: {self.app_key}")
        print(f"DeviceSn: {self.device_sn}")
        print(f"x-token: {headers.get('x-token')}")
        
        # IMPORTANT: Utilise le MÊME body_str que pour la signature
        body_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
        
        response = requests.post(endpoint, data=body_str, headers=headers)  # data= au lieu de json=
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}\n")
            
            if data.get("code") == "0":
                self.token = data.get("data", {}).get("token")
                self.user_id = data.get("data", {}).get("userId")
                print(f"✓ Login successful!")
                print(f"Token: {self.token}")
                print(f"User ID: {self.user_id}")
                return data
            else:
                print(f"[ERROR] {data.get('msg')}")
                return data
        else:
            print(f"[ERROR] HTTP {response.status_code}: {response.text}")
            return None

if __name__ == "__main__":
    print("Starting ThermoMaven Client...")
    
    email = os.getenv('THERMOMAVEN_EMAIL')
    password = os.getenv('THERMOMAVEN_PASSWORD')
    app_key = os.getenv('THERMOMAVEN_APP_KEY')
    app_id = os.getenv('THERMOMAVEN_APP_ID')
    
    if not email or not password or not app_key or not app_id:
        print("[ERROR] Missing environment variables!")
        print("Required: THERMOMAVEN_EMAIL, THERMOMAVEN_PASSWORD, THERMOMAVEN_APP_KEY, THERMOMAVEN_APP_ID")
        exit(1)
    
    client = ThermoMavenClient(email, password)
    client.app_key = app_key
    client.app_id = app_id
    
    result = client.login()
    
    if result and result.get("code") == "0":
        print("\n🎉 SUCCESS! Logged in!")
        print(f"Token: {client.token}")
        print(f"User ID: {client.user_id}")
    else:
        print("\n❌ Failed")