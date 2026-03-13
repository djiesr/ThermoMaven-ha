# 🧪 ThermoMaven v1.4.7 - Fix « indisponible » après connexion

**Release Date:** March 13, 2026  
**Type:** Bug Fix (release candidate)  
**Focus:** Stabilité des capteurs après connexion MQTT

## 🎯 Problème corrigé

Après la connexion, les entités (températures, batterie, etc.) devenaient **indisponibles** quelques secondes plus tard, avec dans les logs :
- `Cannot update device None: device_id=None, devices=1`
- `Probe 1: No lastStatusCmd in device data!`

## 🔧 Modifications techniques

### Ne plus écraser la liste d'appareils par les rapports de température
- **Avant :** Chaque message MQTT (y compris les `status:report` de température) remplaçait la dernière donnée. Un rapport de température arrivant après la liste d'appareils faisait perdre les `deviceId`, d'où `device_id=None` et plus de `lastStatusCmd`.
- **Après :** Seuls les messages `user:device:list` mettent à jour la liste d'appareils. Les rapports de température sont stockés dans un cache par `device_id` et rattachés aux bons appareils à chaque mise à jour.

### Récupération du `deviceId` dans les status:report
- Le `deviceId` est maintenant cherché à la **racine** du message, puis dans **cmdData**, puis déduit du **topic MQTT** si besoin (selon le firmware/API).

### Cas « un seul appareil sans deviceId »
- Si l'API ne renvoie qu'un appareil sans `deviceId` et qu'un seul rapport de statut est reçu, l'intégration associe automatiquement ce rapport à cet appareil.

## 🔄 Installation

### Via HACS
1. **HACS** → **Integrations** → **ThermoMaven**
2. Cliquer sur **Mise à jour** et choisir **v1.4.7**
3. **Redémarrer Home Assistant**

### Mise à jour manuelle
1. Télécharger [v1.4.7](https://github.com/djiesr/thermomaven-ha/releases/tag/v1.4.7)
2. Extraire dans `/config/custom_components/thermomaven/`
3. Redémarrer Home Assistant

## ✅ Résultat attendu

- Les capteurs restent **disponibles** après la réception des rapports MQTT.
- Plus de warnings répétés `Cannot update device None` / `No lastStatusCmd in device data!` dans les logs.

## 📝 Breaking changes

Aucun. Rétrocompatible avec la v1.4.6.

## 🙏 Retour

Merci de signaler tout souci sur [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues).

---

**Full Changelog:** [v1.4.6...v1.4.7](https://github.com/djiesr/thermomaven-ha/compare/v1.4.6...v1.4.7)
