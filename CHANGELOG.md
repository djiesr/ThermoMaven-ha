# Changelog

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

