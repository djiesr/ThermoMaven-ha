# ThermoMaven MQTT Client Guide

Ce guide explique comment utiliser le client MQTT pour se connecter en temps réel aux appareils ThermoMaven.

## 📋 Prérequis

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurer le fichier `.env` (ou `env.copy`) avec vos credentials :
```env
THERMOMAVEN_EMAIL=votre@email.com
THERMOMAVEN_PASSWORD=votre_mot_de_passe
THERMOMAVEN_APP_KEY=bcd4596f1bb8419a92669c8017bf25e8
THERMOMAVEN_APP_ID=ap4060eff28137181bd
```

## 🚀 Utilisation

### Méthode 1 : Script standalone

Lancez le client MQTT :
```bash
python thermomaven_mqtt_client.py
```

Le script va :
1. Se connecter à l'API ThermoMaven
2. Récupérer le certificat MQTT
3. Se connecter au broker MQTT
4. Écouter les messages en temps réel

Appuyez sur `Ctrl+C` pour arrêter.

### Méthode 2 : Utilisation dans votre code

```python
from thermomaven_client import ThermoMavenClient
from thermomaven_mqtt_client import ThermoMavenMQTTClient

# 1. Se connecter à l'API
client = ThermoMavenClient(email, password)
client.app_key = app_key
client.app_id = app_id
client.login()

# 2. Obtenir le certificat MQTT
mqtt_cert = client.get_mqtt_certificate()
mqtt_config = mqtt_cert['data']

# 3. Se connecter au broker MQTT
mqtt_client = ThermoMavenMQTTClient(mqtt_config)
mqtt_client.connect()

# 4. Écouter les messages
mqtt_client.start()  # Bloquant

# Ou en arrière-plan :
mqtt_client.start_background()  # Non-bloquant
```

## 📡 Configuration MQTT

Le certificat MQTT retourne les informations suivantes :

- **p12Url** : URL du certificat P12
- **p12Password** : Mot de passe du certificat
- **clientId** : ID unique du client MQTT (format: `android-{userId}-{region}-{deviceSn}`)
- **subTopics** : Liste des topics à écouter (ex: `app/user/{userId}/sub`)

### Broker MQTT

ThermoMaven utilise **AWS IoT Core** comme broker MQTT.

- **US Region** : `a2ubmaqm3a642j-ats.iot.us-west-2.amazonaws.com`
- **EU Region** : `a2ubmaqm3a642j-ats.iot.eu-central-1.amazonaws.com`
- **Port** : `8883` (SSL/TLS)
- **Protocol** : MQTT v3.1.1

Le client détecte automatiquement votre région à partir du `clientId` retourné par l'API.

## 📨 Messages MQTT

### Types de messages attendus

1. **user:device:list** - Liste des appareils de l'utilisateur
2. **WT:*:status:report** - Rapports de statut des appareils
3. Autres messages de contrôle et notifications

### Format des messages

Les messages MQTT sont au format JSON. Exemple :

```json
{
  "cmdType": "user:device:list",
  "data": [
    {
      "deviceId": "...",
      "deviceName": "...",
      "deviceModel": "WT02",
      "deviceSn": "...",
      ...
    }
  ]
}
```

## 🔐 Sécurité

Le client MQTT utilise SSL/TLS avec authentification par certificat client :

1. Le certificat P12 est téléchargé depuis l'API
2. Il est converti en format PEM (certificat + clé privée)
3. Ces fichiers sont utilisés pour l'authentification SSL
4. Les fichiers temporaires sont supprimés à la déconnexion

### Conversion P12 vers PEM

La conversion nécessite `pyOpenSSL`. Si non disponible, le client tentera une connexion SSL sans certificat client (peut échouer selon la configuration du broker).

## 🐛 Dépannage

### "pyOpenSSL not installed"

Installez pyOpenSSL :
```bash
pip install pyOpenSSL
```

### "Connection refused - not authorized"

Vérifiez :
- Que vous êtes bien connecté à l'API (token valide)
- Que le certificat a été téléchargé et converti correctement
- Que le clientId correspond bien à celui fourni par l'API

### "Connection timeout"

Vérifiez :
- Votre connexion Internet
- Que le broker est accessible : `mqtt.iot.thermomaven.com:8883`
- Que le port 8883 n'est pas bloqué par votre firewall

### Aucun message reçu

C'est normal si :
- Vous n'avez pas d'appareil lié à votre compte
- Vos appareils ne sont pas allumés
- Vos appareils ne sont pas connectés au WiFi

Pour recevoir des messages :
1. Assurez-vous d'avoir au moins un appareil ThermoMaven lié
2. Allumez l'appareil
3. Connectez-le au WiFi
4. Les messages devraient commencer à arriver

## 📊 Callbacks personnalisés

Vous pouvez personnaliser le traitement des messages :

```python
def custom_message_handler(client, userdata, msg):
    print(f"Received: {msg.payload.decode()}")
    # Votre traitement personnalisé ici

mqtt_client = ThermoMavenMQTTClient(mqtt_config)
mqtt_client.client.on_message = custom_message_handler
mqtt_client.connect()
mqtt_client.start()
```

## 🔄 Publier des messages

Pour envoyer des commandes aux appareils :

```python
# Publier sur un topic
mqtt_client.client.publish("app/device/{deviceId}/cmd", json.dumps({
    "cmdType": "set_temperature",
    "value": 65
}))
```

**Note** : La documentation complète des commandes MQTT disponibles n'est pas encore établie.

## 📚 Ressources

- [API Endpoints Documentation](API_ENDPOINTS.md)
- [Paho MQTT Documentation](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)
- [MQTT Protocol](https://mqtt.org/)

