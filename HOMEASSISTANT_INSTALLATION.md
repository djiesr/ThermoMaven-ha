# Installation de l'intégration ThermoMaven dans Home Assistant

## 📋 Prérequis

- Home Assistant Core 2023.1 ou supérieur
- Compte ThermoMaven avec au moins un appareil configuré
- Accès au dossier `config` de Home Assistant

## 🚀 Installation

### Méthode 1 : Installation Manuelle (Recommandée pour test)

1. **Copier les fichiers**
   
   Copiez le dossier `custom_components/thermomaven` dans le répertoire `config/custom_components/` de votre Home Assistant.
   
   Structure finale :
   ```
   config/
   └── custom_components/
       └── thermomaven/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           ├── strings.json
           ├── thermomaven_api.py
           ├── translations/
           │   ├── en.json
           │   └── fr.json
           └── README.md
   ```

2. **Redémarrer Home Assistant**
   
   Allez dans **Paramètres** → **Système** → **Redémarrer**

3. **Vérifier les logs**
   
   Vérifiez qu'il n'y a pas d'erreurs dans les logs :
   **Paramètres** → **Système** → **Journaux**

### Méthode 2 : Via HACS (Futur)

Une fois publié sur HACS, vous pourrez installer via :
1. HACS → Intégrations
2. Menu (⋮) → Dépôts personnalisés
3. Ajouter l'URL du repository
4. Rechercher "ThermoMaven"
5. Installer

## ⚙️ Configuration

### Ajouter l'intégration

1. **Aller dans Intégrations**
   
   **Paramètres** → **Appareils et Services** → **+ Ajouter une intégration**

2. **Rechercher ThermoMaven**
   
   Tapez "ThermoMaven" dans la barre de recherche

3. **Entrer vos identifiants**
   
   - **Email** : Votre email ThermoMaven
   - **Mot de passe** : Votre mot de passe ThermoMaven

4. **Attendre la connexion**
   
   L'intégration va :
   - Se connecter à l'API ThermoMaven
   - Récupérer le certificat MQTT
   - Se connecter au broker AWS IoT
   - Découvrir vos appareils

5. **Vérifier les entités créées**
   
   Allez dans **Paramètres** → **Appareils et Services** → **ThermoMaven**
   
   Vous devriez voir vos appareils avec leurs sondes de température et batterie.

## 🔧 Configuration Avancée

### Personnaliser les noms d'entités

1. Allez dans **Paramètres** → **Appareils et Services** → **ThermoMaven**
2. Cliquez sur un appareil
3. Cliquez sur une entité
4. Cliquez sur l'icône de paramètres (⚙️)
5. Modifiez le nom ou l'ID d'entité

### Désactiver les mises à jour automatiques

Par défaut, l'intégration utilise MQTT pour les mises à jour en temps réel.
Si vous souhaitez désactiver cela, vous devrez modifier le code.

## 📊 Utilisation dans Lovelace

### Carte simple

```yaml
type: entities
title: Mon BBQ
entities:
  - entity: sensor.thermomaven_grill_probe_1
    name: Température Viande
    icon: mdi:food-steak
  - entity: sensor.thermomaven_grill_probe_2
    name: Température Ambiante
    icon: mdi:thermometer
  - entity: sensor.thermomaven_grill_battery
    name: Batterie
```

### Carte Graphique

```yaml
type: history-graph
title: Historique Températures
entities:
  - sensor.thermomaven_grill_probe_1
  - sensor.thermomaven_grill_probe_2
hours_to_show: 3
refresh_interval: 0
```

### Carte Gauge

```yaml
type: gauge
entity: sensor.thermomaven_grill_probe_1
name: Température Actuelle
unit: °C
severity:
  green: 0
  yellow: 50
  red: 70
min: 0
max: 100
```

## 🤖 Automatisations

### Alerte quand la température est atteinte

```yaml
automation:
  - alias: "Alerte BBQ - Viande prête"
    trigger:
      - platform: numeric_state
        entity_id: sensor.thermomaven_grill_probe_1
        above: 60
    condition:
      - condition: state
        entity_id: input_boolean.bbq_en_cours
        state: "on"
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "🍖 BBQ"
          message: "La viande est prête ! ({{ states('sensor.thermomaven_grill_probe_1') }}°C)"
          data:
            push:
              sound: "US-EN-Alexa-Temperature-Reached.wav"
```

### Notification batterie faible

```yaml
automation:
  - alias: "ThermoMaven - Batterie faible"
    trigger:
      - platform: numeric_state
        entity_id: sensor.thermomaven_grill_battery
        below: 20
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Batterie faible"
          message: "Le thermomètre {{ state_attr('sensor.thermomaven_grill_battery', 'friendly_name') }} a une batterie faible ({{ states('sensor.thermomaven_grill_battery') }}%)"
```

## 🔍 Dépannage

### L'intégration ne charge pas

1. **Vérifier les logs**
   ```
   Paramètres → Système → Journaux
   ```
   Recherchez "thermomaven" ou "custom_components"

2. **Vérifier les dépendances**
   Les dépendances suivantes doivent être installées :
   - `paho-mqtt>=1.6.1`
   - `cryptography>=41.0.0`

3. **Vérifier la structure des fichiers**
   Assurez-vous que tous les fichiers sont dans le bon dossier.

### Pas d'appareils découverts

1. **Vérifier que vos appareils sont liés**
   - Ouvrez l'app mobile ThermoMaven
   - Vérifiez que vos thermomètres sont bien visibles

2. **Recharger l'intégration**
   ```
   Paramètres → Appareils et Services → ThermoMaven → ⋮ → Recharger
   ```

3. **Vérifier les credentials**
   - Email et mot de passe corrects
   - Compte actif

### MQTT ne se connecte pas

1. **Vérifier les certificats**
   - Les certificats sont téléchargés automatiquement
   - Vérifiez les logs pour des erreurs de conversion P12

2. **Vérifier la connexion Internet**
   - Home Assistant doit pouvoir accéder à AWS IoT Core
   - Ports : 8883 (MQTT SSL)

3. **Tester manuellement**
   Utilisez le script standalone :
   ```bash
   python thermomaven_mqtt_client.py
   ```

### Les températures ne se mettent pas à jour

1. **Vérifier que les appareils sont allumés**
2. **Vérifier la connexion MQTT dans les logs**
3. **Redémarrer l'intégration**

## 📝 Logs Utiles

Pour activer les logs détaillés, ajoutez dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.thermomaven: debug
    paho.mqtt: debug
```

Puis redémarrez Home Assistant.

## 🆘 Support

- **Issues GitHub** : [Créer une issue](https://github.com/yourusername/thermomaven-homeassistant/issues)
- **Forum Home Assistant** : Tag `thermomaven`
- **Discord** : Canal #custom-components

## 📖 Documentation Additionnelle

- [README Principal](README.md)
- [API Documentation](API_ENDPOINTS.md)
- [MQTT Guide](MQTT_GUIDE.md)

