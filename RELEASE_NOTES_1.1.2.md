# ThermoMaven v1.1.2 - Découverte Automatique des Devices 🎉

## 🐛 Problème Résolu

**Avant** : Il fallait ouvrir l'application mobile ThermoMaven pour que les thermomètres soient détectés dans Home Assistant. Une fois détectés, tout fonctionnait bien même en fermant l'app.

**Maintenant** : Les thermomètres sont **détectés automatiquement** au démarrage de Home Assistant, **sans avoir besoin d'ouvrir l'application mobile** ! 🚀

## 🔍 Explication Technique

Le système ThermoMaven utilise une architecture hybride REST API + MQTT :

### Comment ça fonctionne :
1. **MQTT** : Canal de communication pour les mises à jour en temps réel (température, statut, batterie)
2. **REST API** : Utilisée pour déclencher certaines actions côté serveur

### Le Problème Découvert :
Le message MQTT `user:device:list` (qui contient la liste des thermomètres) **n'est publié par le serveur que lorsqu'un client appelle les endpoints API de listing** :
- `/app/device/share/my/device/list`
- `/app/device/share/shared/device/list`

L'application mobile appelle automatiquement ces endpoints au démarrage, ce qui déclenche l'envoi du message MQTT. L'intégration Home Assistant, elle, se connectait au MQTT mais **attendait passivement** ce message sans jamais le déclencher.

### La Solution :
L'intégration appelle maintenant **activement** les endpoints API pour déclencher l'envoi du message `user:device:list`, exactement comme le fait l'application mobile.

## ✨ Améliorations Apportées

### 1. Synchronisation Automatique à la Connexion MQTT
Dès que l'intégration se connecte au broker MQTT, elle déclenche automatiquement la synchronisation des devices.

### 2. Synchronisation Initiale Garantie
Après la configuration MQTT, une synchronisation supplémentaire est déclenchée (avec un délai de 2 secondes pour assurer la stabilité de la connexion).

### 3. Synchronisation de Secours avec Protection Anti-Spam
Si aucun device n'est découvert lors d'une mise à jour du coordinator, une nouvelle synchronisation est automatiquement déclenchée. 

**Protection anti-spam** :
- Maximum **3 tentatives automatiques** (toutes les 5 minutes)
- Évite de surcharger l'API si aucun thermomètre n'est allumé
- Le compteur se réinitialise dès qu'un device est détecté

### 4. Service Manuel de Synchronisation
Un nouveau service Home Assistant est disponible : **`thermomaven.sync_devices`**

**Comment l'utiliser** :
1. Outils de développement → Services
2. Chercher "ThermoMaven: Synchroniser les appareils"
3. Cliquer sur "Appeler le service"

**Quand l'utiliser** :
- Si tes thermomètres ne sont pas détectés automatiquement
- Après avoir allumé un nouveau thermomètre
- Si tu as atteint la limite de 3 tentatives automatiques

**Dans une automation** :
```yaml
service: thermomaven.sync_devices
```

## 🎯 Comment Tester

1. **Supprimez** l'intégration ThermoMaven existante dans Home Assistant
2. **Redémarrez** Home Assistant
3. **Réinstallez** l'intégration ThermoMaven
4. **Attendez** 10-15 secondes
5. **Les thermomètres apparaissent automatiquement** ! ✅

**Important** : Vous n'avez **PLUS BESOIN** d'ouvrir l'application mobile !

## 📊 Comportement Attendu

| Action | Avant | Après |
|--------|-------|-------|
| Démarrage de HA | ❌ Pas de devices | ✅ Devices détectés automatiquement |
| Besoin de l'app mobile | ⚠️ Obligatoire pour découverte | ✅ Optionnel |
| Temps de découverte | Variable | 10-15 secondes |
| Retry automatique | ❌ Non | ✅ Oui (max 3 tentatives) |
| Synchronisation manuelle | ❌ Non disponible | ✅ Service `thermomaven.sync_devices` |
| Protection anti-spam | ❌ Appels infinis | ✅ Limite de 3 tentatives |

## 📝 Fichiers Modifiés

- `thermomaven_api.py` :
  - Ajout de la méthode `_trigger_device_sync()`
  - Modification de `_on_mqtt_connect()` pour déclencher la sync
  - Modification de `async_setup_mqtt()` pour sync initiale

- `__init__.py` :
  - Modification de `_async_update_data()` pour sync de secours avec compteur de tentatives
  - Enregistrement du service `sync_devices`
  - Désenregistrement du service au unload

- `services.yaml` : Définition du service `sync_devices`

- `strings.json` : Traductions du service

- `manifest.json` : Version 1.1.1 → 1.1.2

- Documentation :
  - `DEVICE_DISCOVERY_FIX.md` : Documentation technique détaillée
  - `CHANGELOG.md` : Entrée complète pour v1.1.2

## 🎉 Résultat

L'intégration ThermoMaven est maintenant **100% autonome** et ne dépend plus de l'application mobile pour la découverte des devices !

## 🆘 En Cas de Problème

Si les devices ne sont pas détectés, vérifiez les logs de Home Assistant :

```
Paramètres → Système → Logs
```

Recherchez les entrées contenant :
- `Connected to MQTT broker`
- `Triggering device list synchronization via API`
- `Device sync triggered successfully`
- `MQTT device list: X devices found`
- `No devices found, triggering MQTT sync (attempt X/3)`
- `Max auto-sync attempts reached. Use 'thermomaven.sync_devices' service to retry manually.`

**Solutions** :
1. Si tu vois "Max auto-sync attempts reached", utilise le service `thermomaven.sync_devices`
2. Assure-toi que ton thermomètre est allumé et connecté au WiFi
3. Si le problème persiste, contacte le support via GitHub Issues

## 📚 Documentation Complète

Pour plus de détails techniques, consultez :
- `DEVICE_DISCOVERY_FIX.md` : Explication approfondie du problème et de la solution
- `CHANGELOG.md` : Historique complet des versions
- `README.md` : Guide d'installation et d'utilisation

---

**Bonne utilisation de ThermoMaven v1.1.2 !** 🌡️🔥

