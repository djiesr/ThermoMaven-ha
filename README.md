# ThermoMaven API Client

Un client Python non officiel pour interagir avec l'API ThermoMaven IoT.

## Description

Ce projet fournit un client Python pour communiquer avec l'API ThermoMaven, permettant de contrôler et surveiller les appareils de cuisine connectés ThermoMaven.

## Caractéristiques

- Authentification sécurisée avec l'API ThermoMaven
- Génération automatique des signatures requises
- Support de plusieurs régions (US, EU, etc.)
- Client HTTP configurable

## Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/votre-username/ThermoMaven.git
cd ThermoMaven
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

Créez un fichier `.env` à la racine du projet avec vos identifiants :

```env
THERMOMAVEN_EMAIL=votre-email@example.com
THERMOMAVEN_PASSWORD=votre-mot-de-passe
THERMOMAVEN_APP_KEY=votre-app-key
```

## Utilisation

```python
from thermomaven_client import ThermoMavenClient
import os

# Initialiser le client
client = ThermoMavenClient(
    email=os.getenv('THERMOMAVEN_EMAIL'),
    password=os.getenv('THERMOMAVEN_PASSWORD')
)

# Configurer l'app key (à trouver)
client.app_key = os.getenv('THERMOMAVEN_APP_KEY', '')

# Se connecter
result = client.login()

if result:
    print("Connexion réussie!")
    # Votre code ici...
else:
    print("Échec de la connexion")
```

## Documentation API

Le dossier `whatweknow/` contient des informations extraites sur l'API ThermoMaven :

- `part1.txt` : Configuration de l'API (endpoints MQTT, régions, versions)
- `part2.txt` : Liste des endpoints disponibles

### Endpoints principaux

- `/app/account/login` - Authentification
- `/app/device/*` - Gestion des appareils
- `/app/user/*` - Gestion utilisateur
- `/app/history/*` - Historique des données
- `/app/recipe/*` - Recettes
- `/app/mqtt/cert/apply` - Certificats MQTT

### Régions supportées

Le service utilise deux centres de données :
- **US** : `https://api.iot.thermomaven.com` (États-Unis, Canada, Australie, etc.)
- **DE** : `https://api.iot.thermomaven.de` (Europe, UK, etc.)

## Structure du projet

```
ThermoMaven/
├── thermomaven_client.py    # Client API principal
├── whatweknow/              # Documentation de l'API
│   ├── part1.txt           # Configuration et régions
│   └── part2.txt           # Endpoints disponibles
├── requirements.txt         # Dépendances Python
├── .gitignore              # Fichiers à ignorer
└── README.md               # Ce fichier
```

## Sécurité

⚠️ **Important** : Ne commitez jamais vos identifiants dans le code. Utilisez toujours des variables d'environnement ou un fichier `.env` (qui doit être dans `.gitignore`).

## Avertissement

Ce projet est non officiel et n'est pas affilié à ThermoMaven. Utilisez-le à vos propres risques. L'utilisation de ce client peut violer les conditions d'utilisation de ThermoMaven.

## Licence

Ce projet est fourni "tel quel" à des fins éducatives uniquement.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## À faire

- [ ] Trouver l'`app_key` valide
- [ ] Implémenter les autres endpoints (appareils, historique, etc.)
- [ ] Ajouter le support MQTT
- [ ] Créer des tests unitaires
- [ ] Ajouter la documentation des modèles de données

