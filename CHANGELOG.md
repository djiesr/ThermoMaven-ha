# Changelog

## [1.0.3] - 2025-10-12 - Device Topic Subscription & MQTT Optimization

### ✨ New Features
- **Automatic device topic subscription**: Integration now subscribes to individual device topics for real-time updates
  - When devices are discovered, their specific topics (`subTopics`) are automatically subscribed
  - Enables direct device-to-integration communication
  - Better real-time temperature updates

### 🔧 Improvements
- **MQTT-first approach**: Reduced polling interval from 60s to 300s (5 minutes)
  - MQTT is now the primary data source for real-time updates
  - API polling is now a fallback mechanism
  - Reduces API calls and improves responsiveness
  
- **Enhanced logging**:
  - MQTT messages now log the topic they were received on
  - Device topic subscriptions are logged for debugging
  - Temperature update messages include cmdType for better tracking

### 📝 Technical Details
- `custom_components/thermomaven/thermomaven_api.py`:
  - Added automatic subscription to device `subTopics` on device list updates
  - Enhanced logging with topic information in MQTT message handler
  - Improved temperature update logging with cmdType

- `custom_components/thermomaven/__init__.py`:
  - Update interval changed from 60s to 300s (MQTT is primary)
  - Added comment clarifying MQTT-first approach

### 🎯 Benefits
- Faster response to temperature changes (MQTT push vs API polling)
- Reduced server load with fewer API calls
- More reliable real-time data from devices
- Better debugging with enhanced logging

### 🔄 How It Works
```
1. Device list received via MQTT
2. Extract subTopics for each device
3. Subscribe to each device's specific topics
4. Receive real-time updates directly from devices
5. Fallback to API polling every 5 minutes if needed
```

---

## [1.0.2] - 2025-10-12 - Dynamic Device Discovery

### ✨ New Features
- **Dynamic device addition**: Devices are now automatically detected and added when they become available
  - No need to restart Home Assistant when a new device comes online
  - Devices detected via MQTT are automatically added to the integration
  - Prevents duplicate entity creation

### 🔧 Improvements
- **Smart device tracking**: Integration now tracks which devices have been added
  - Uses device ID tracking to prevent duplicates
  - Callback system for real-time device discovery
  - Better handling of devices appearing/disappearing

### 📝 Technical Details
- `custom_components/thermomaven/sensor.py`:
  - Added `added_devices` set to track registered devices
  - Created `add_devices()` function for dynamic device addition
  - Registered coordinator listener for automatic updates
  - Added debug logging for device discovery
  - Prevents duplicate entity warnings

### 🎯 Benefits
- Devices automatically appear when they connect via MQTT
- No more "entity already registered" warnings
- Better support for multiple devices
- Seamless device detection in real-time

### 🔄 File Organization
- Moved `whatweknow/` folder to `api/whatweknow/` for better structure

---

## [1.0.1] - 2025-10-12 - Logging Improvements

### 🔧 Improvements
- **Enhanced logging**: Added detailed debug and info logs for device retrieval
  - Log device count from API responses
  - Log MQTT data processing with cmdType information
  - Log final device count after merging API and MQTT data
  - Log device details in MQTT messages for better debugging
  - Warning when MQTT device list is empty

### 🐛 Bug Fixes
- Better error tracking for empty device lists
- More informative logs when MQTT data is processed

### 📝 Technical Details
- `custom_components/thermomaven/__init__.py`:
  - Added debug logging for API device count
  - Added debug logging for MQTT cmdType
  - Added info logging for MQTT device count
  - Added warning for empty MQTT device lists
  - Added final device count logging

- `custom_components/thermomaven/thermomaven_api.py`:
  - Enhanced MQTT device list logging with device count
  - Added debug logging with full device data in JSON format

These improvements make it much easier to diagnose issues with device detection and MQTT integration.

---

## [1.0.0] - 2025-10-12 - Initial Release - MQTT Support & API Improvements

### ✨ Nouveautés

#### Client MQTT
- Ajout du client MQTT (`thermomaven_mqtt_client.py`) pour la communication en temps réel
- Support des certificats P12 avec conversion automatique en PEM
- Écoute automatique des topics MQTT pour recevoir les updates des appareils
- Gestion des callbacks pour les messages, connexion, déconnexion

#### Nouveaux Endpoints API
- `get_mqtt_certificate()` - Récupère le certificat MQTT et la configuration
- `get_device_models()` - Liste tous les modèles d'appareils disponibles (WT02, WT06, WT07, WT09, WT10, WT11)
- `get_notification_devices()` - Liste des appareils pour les notifications
- `get_history_page()` - Historique des cuissons avec pagination (CORRIGÉ: utilise "current" et "size")
- `get_my_devices()` - Liste des appareils que vous possédez
- `get_shared_devices()` - Liste des appareils partagés avec vous

#### Améliorations du Client REST
- Méthode générique `_make_request()` pour toutes les requêtes authentifiées
- Résumé automatique des résultats des endpoints testés
- Meilleur affichage des réponses JSON avec formatage

#### Documentation
- `API_ENDPOINTS.md` - Documentation complète de tous les endpoints découverts
- `MQTT_GUIDE.md` - Guide d'utilisation du client MQTT
- `CHANGELOG.md` - Ce fichier

### 🔧 Corrections
- Correction de l'endpoint `get_history_page()` : utilise maintenant les bons paramètres ("current" et "size" au lieu de "page" et "pageSize")
- Les endpoints de liste d'appareils utilisent maintenant les bons chemins (`/app/device/share/my/device/list` et `/app/device/share/shared/device/list`)

### 📦 Dépendances ajoutées
- `paho-mqtt>=1.6.1` - Client MQTT
- `pyOpenSSL>=23.0.0` - Conversion de certificats P12 vers PEM

### 📊 Modèles d'appareils supportés
- **WT02** - ThermoMaven P2 (2 sondes)
- **WT06** - ThermoMaven P4 (4 sondes)
- **WT07** - ThermoMaven G2 (2 sondes)
- **WT09** - ThermoMaven G4 (4 sondes)
- **WT10** - ThermoMaven G1 (1 sonde)
- **WT11** - ThermoMaven P1 (1 sonde)

### 🔐 Sécurité
- Authentification MQTT via certificats SSL/TLS client
- Gestion automatique des certificats temporaires
- Nettoyage automatique des fichiers sensibles

### 🐛 Problèmes connus
- Les endpoints de liste d'appareils (`/app/device/share/my/device/list`, etc.) retournent des listes vides si aucun appareil n'est lié au compte
- La connexion MQTT nécessite pyOpenSSL pour la conversion P12→PEM
- Les messages MQTT ne sont reçus que si des appareils sont connectés et actifs

### 📝 Notes
- Les appareils ThermoMaven communiquent principalement via MQTT plutôt que via API REST
- Le topic MQTT principal est `app/user/{userId}/sub`
- Les messages MQTT utilisent le type `user:device:list` pour la liste des appareils
- Les rapports de statut utilisent le pattern `WT:*:status:report`

## Prochaines étapes

- [ ] Découvrir les commandes MQTT pour contrôler les appareils
- [ ] Implémenter la lecture en temps réel des températures
- [ ] Ajouter le support des recettes et collections
- [ ] Explorer les fonctionnalités OTA (mises à jour firmware)
- [ ] Documenter les formats de messages MQTT

