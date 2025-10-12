import paho.mqtt.client as mqtt
import ssl
import json
import os
import requests
import tempfile
from thermomaven_client import ThermoMavenClient
from dotenv import load_dotenv

try:
    from OpenSSL import crypto
    OPENSSL_AVAILABLE = True
except ImportError:
    OPENSSL_AVAILABLE = False
    print("⚠️  pyOpenSSL not installed. P12 certificate conversion not available.")

# Charger les variables d'environnement
load_dotenv()

class ThermoMavenMQTTClient:
    def __init__(self, mqtt_config):
        """
        Initialise le client MQTT avec la configuration reçue de l'API
        
        Args:
            mqtt_config: Dict contenant p12Url, p12Password, clientId, subTopics
        """
        self.mqtt_config = mqtt_config
        self.client_id = mqtt_config['clientId']
        self.sub_topics = mqtt_config['subTopics']
        self.p12_url = mqtt_config['p12Url']
        self.p12_password = mqtt_config['p12Password']
        
        # Broker MQTT - AWS IoT Core endpoints (trouvés dans les assets de l'APK)
        # Le client ID contient la région (US ou EU), on va l'extraire
        region = self._extract_region_from_client_id(self.client_id)
        
        self.broker_endpoints = {
            "US": "a2ubmaqm3a642j-ats.iot.us-west-2.amazonaws.com",
            "EU": "a2ubmaqm3a642j-ats.iot.eu-central-1.amazonaws.com",
        }
        
        self.broker = self.broker_endpoints.get(region, self.broker_endpoints["US"])
        self.port = 8883  # Port SSL standard pour MQTT
        self.region = region
        
        print(f"📍 Detected region: {region}")
        print(f"🌐 Using MQTT broker: {self.broker}")
        
        self.client = None
        self.p12_file_path = None
        self.cert_file_path = None
        self.key_file_path = None
    
    def _extract_region_from_client_id(self, client_id):
        """Extrait la région du client ID (format: android-{userId}-{region}-{deviceSn})"""
        try:
            parts = client_id.split('-')
            if len(parts) >= 3:
                # Le format est android-{userId}-{region}-{deviceSn}
                region = parts[2]
                if region in ["US", "EU"]:
                    return region
        except:
            pass
        return "US"  # Défaut
        
    def download_certificate(self):
        """Télécharge le certificat P12"""
        print(f"\n📥 Downloading P12 certificate from {self.p12_url}")
        
        response = requests.get(self.p12_url)
        if response.status_code == 200:
            # Créer un fichier temporaire pour le certificat
            with tempfile.NamedTemporaryFile(delete=False, suffix='.p12') as f:
                f.write(response.content)
                self.p12_file_path = f.name
                print(f"✓ Certificate downloaded to {self.p12_file_path}")
                return True
        else:
            print(f"✗ Failed to download certificate: {response.status_code}")
            return False
    
    def convert_p12_to_pem(self):
        """Convertit le certificat P12 en fichiers PEM (cert + key)"""
        if not OPENSSL_AVAILABLE:
            print("⚠️  Cannot convert P12: pyOpenSSL not installed")
            print("    Install it with: pip install pyOpenSSL")
            return False
        
        if not self.p12_file_path:
            print("✗ No P12 file to convert")
            return False
        
        print("\n🔄 Converting P12 to PEM format...")
        
        try:
            # Lire le fichier P12
            with open(self.p12_file_path, 'rb') as f:
                p12_data = f.read()
            
            # Charger le P12 - syntaxe mise à jour pour pyOpenSSL moderne
            try:
                # Nouvelle API (pyOpenSSL >= 23.x)
                from cryptography.hazmat.primitives.serialization import pkcs12
                private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                    p12_data, 
                    self.p12_password.encode()
                )
                
                # Convertir en PEM
                from cryptography.hazmat.primitives import serialization
                
                cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
                key_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
            except ImportError:
                # Ancienne API (pyOpenSSL < 23.x)
                p12 = crypto.load_pkcs12(p12_data, self.p12_password.encode())
                cert_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
                key_pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
            
            # Sauvegarder le certificat
            with tempfile.NamedTemporaryFile(delete=False, suffix='.crt', mode='wb') as f:
                f.write(cert_pem)
                self.cert_file_path = f.name
            
            # Sauvegarder la clé
            with tempfile.NamedTemporaryFile(delete=False, suffix='.key', mode='wb') as f:
                f.write(key_pem)
                self.key_file_path = f.name
            
            print(f"✓ Certificate converted to PEM")
            print(f"  Cert: {self.cert_file_path}")
            print(f"  Key: {self.key_file_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error converting P12 to PEM: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback quand le client se connecte au broker"""
        if rc == 0:
            print(f"\n✓ Connected to MQTT broker!")
            print(f"Client ID: {self.client_id}")
            
            # S'abonner aux topics
            for topic in self.sub_topics:
                print(f"📡 Subscribing to topic: {topic}")
                client.subscribe(topic)
                print(f"✓ Subscribed to {topic}")
        else:
            print(f"\n✗ Failed to connect to MQTT broker, return code {rc}")
            error_messages = {
                1: "Connection refused - incorrect protocol version",
                2: "Connection refused - invalid client identifier",
                3: "Connection refused - server unavailable",
                4: "Connection refused - bad username or password",
                5: "Connection refused - not authorized"
            }
            print(f"Error: {error_messages.get(rc, 'Unknown error')}")
    
    def on_message(self, client, userdata, msg):
        """Callback quand un message est reçu"""
        print(f"\n📨 Message received on topic: {msg.topic}")
        print(f"Payload: {msg.payload.decode('utf-8', errors='replace')}")
        
        try:
            # Essayer de parser le JSON
            data = json.loads(msg.payload.decode('utf-8'))
            print(f"\n📦 Parsed JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Détecter le type de message
            if 'cmdType' in data:
                cmd_type = data['cmdType']
                print(f"\n🔔 Command Type: {cmd_type}")
                
                if cmd_type == "user:device:list":
                    print("\n🎉 DEVICE LIST RECEIVED!")
                    if 'data' in data or 'cmdData' in data:
                        print(json.dumps(data.get('data') or data.get('cmdData'), indent=2))
                        
        except json.JSONDecodeError:
            print("⚠️  Payload is not valid JSON")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback quand le client se déconnecte"""
        if rc != 0:
            print(f"\n⚠️  Unexpected disconnection (code {rc})")
        else:
            print(f"\n✓ Disconnected from MQTT broker")
    
    def on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback quand la souscription est confirmée"""
        print(f"✓ Subscription confirmed (QoS: {granted_qos})")
    
    def connect(self):
        """Se connecte au broker MQTT AWS IoT Core"""
        # Télécharger le certificat
        if not self.download_certificate():
            return False
        
        # Convertir P12 en PEM (obligatoire pour AWS IoT)
        if not self.convert_p12_to_pem():
            print("\n✗ P12 conversion failed - cannot connect to AWS IoT without certificate")
            return False
        
        print(f"\n🔌 Connecting to AWS IoT broker: {self.broker}:{self.port}")
        print(f"   Client ID: {self.client_id}")
        
        try:
            # Créer le client MQTT
            self.client = mqtt.Client(
                client_id=self.client_id, 
                protocol=mqtt.MQTTv311,
                callback_api_version=mqtt.CallbackAPIVersion.VERSION1
            )
            
            # Configurer les callbacks
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            self.client.on_subscribe = self.on_subscribe
            
            # Configurer SSL/TLS avec le certificat client (requis pour AWS IoT)
            print("🔐 Configuring TLS with client certificate")
            self.client.tls_set(
                certfile=self.cert_file_path,
                keyfile=self.key_file_path,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
            
            # Connexion au broker AWS IoT
            self.client.connect(self.broker, self.port, keepalive=60)
            
            print(f"✓ Connection initiated, waiting for acknowledgment...")
            return True
            
        except Exception as e:
            print(f"\n✗ Failed to connect to AWS IoT broker: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start(self):
        """Démarre la boucle MQTT (bloquant)"""
        if self.client:
            print("\n🎧 Listening for MQTT messages... (Press Ctrl+C to stop)")
            try:
                self.client.loop_forever()
            except KeyboardInterrupt:
                print("\n\n⏹️  Stopping MQTT client...")
                self.disconnect()
    
    def start_background(self):
        """Démarre la boucle MQTT en arrière-plan (non-bloquant)"""
        if self.client:
            print("\n🎧 Starting MQTT client in background...")
            self.client.loop_start()
    
    def disconnect(self):
        """Se déconnecte du broker MQTT"""
        if self.client:
            self.client.disconnect()
            self.client.loop_stop()
        
        # Nettoyer les fichiers temporaires
        for file_path in [self.p12_file_path, self.cert_file_path, self.key_file_path]:
            if file_path and os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f"⚠️  Could not delete {file_path}: {e}")
        
        print("✓ Cleaned up temporary certificate files")


if __name__ == "__main__":
    print("="*70)
    print("ThermoMaven MQTT Client")
    print("="*70)
    
    # Charger les credentials
    email = os.getenv('THERMOMAVEN_EMAIL')
    password = os.getenv('THERMOMAVEN_PASSWORD')
    app_key = os.getenv('THERMOMAVEN_APP_KEY')
    app_id = os.getenv('THERMOMAVEN_APP_ID')
    
    if not all([email, password, app_key, app_id]):
        print("[ERROR] Missing environment variables!")
        exit(1)
    
    # Se connecter à l'API REST pour obtenir le certificat MQTT
    print("\n📡 Step 1: Login to ThermoMaven API...")
    client = ThermoMavenClient(email, password)
    client.app_key = app_key
    client.app_id = app_id
    
    result = client.login()
    
    if not result or result.get("code") != "0":
        print("\n✗ Failed to login")
        exit(1)
    
    print("\n✓ Login successful!")
    
    # Obtenir le certificat MQTT
    print("\n📡 Step 2: Get MQTT certificate...")
    mqtt_cert = client.get_mqtt_certificate()
    
    if not mqtt_cert or mqtt_cert.get("code") != "0":
        print("\n✗ Failed to get MQTT certificate")
        exit(1)
    
    mqtt_config = mqtt_cert['data']
    print("\n✓ MQTT certificate obtained!")
    print(f"Client ID: {mqtt_config['clientId']}")
    print(f"Subscribe Topics: {mqtt_config['subTopics']}")
    
    # Se connecter au broker MQTT
    print("\n📡 Step 3: Connect to MQTT broker...")
    mqtt_client = ThermoMavenMQTTClient(mqtt_config)
    
    if mqtt_client.connect():
        # Démarrer l'écoute des messages
        mqtt_client.start()
    else:
        print("\n✗ Failed to connect to MQTT broker")
        exit(1)

