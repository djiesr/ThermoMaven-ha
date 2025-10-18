# Service de Synchronisation Manuelle

## 🔄 thermomaven.sync_devices

Ce service permet de forcer la synchronisation de la liste des thermomètres ThermoMaven.

## 📖 Utilisation

### Dans l'Interface Home Assistant

1. Ouvre **Outils de développement** (Developer Tools)
2. Va dans l'onglet **Services**
3. Cherche **"ThermoMaven: Synchroniser les appareils"** ou tape `thermomaven.sync_devices`
4. Clique sur **"Appeler le service"** (Call Service)

### Dans une Automation

```yaml
automation:
  - alias: "Sync ThermoMaven au démarrage"
    trigger:
      - platform: homeassistant
        event: start
    action:
      - delay: "00:00:30"  # Attendre 30s après le démarrage
      - service: thermomaven.sync_devices
```

### Dans un Script

```yaml
script:
  sync_thermomaven:
    alias: "Synchroniser ThermoMaven"
    sequence:
      - service: thermomaven.sync_devices
```

### Via Node-RED

```json
{
  "domain": "thermomaven",
  "service": "sync_devices"
}
```

## 🎯 Quand Utiliser ce Service

### Situations Recommandées

✅ **Après avoir allumé un nouveau thermomètre**
- Le service va déclencher la découverte du nouveau device

✅ **Si aucun thermomètre n'est détecté au démarrage**
- Attends 30 secondes puis appelle le service

✅ **Quand tu vois le message "Max auto-sync attempts reached" dans les logs**
- Le système a atteint la limite de 3 tentatives automatiques
- Utilise le service pour réinitialiser le compteur et forcer une nouvelle sync

✅ **Après une panne WiFi ou MQTT**
- Pour s'assurer que tous les thermomètres sont re-découverts

### Situations NON Recommandées

❌ **Appels trop fréquents**
- Évite d'appeler ce service en boucle (ça spam l'API ThermoMaven)
- L'intégration fait déjà 3 tentatives automatiques

❌ **Si les thermomètres sont déjà détectés**
- Pas besoin, les mises à jour se font automatiquement via MQTT

❌ **Pendant une cuisson active**
- Les températures se mettent à jour automatiquement via MQTT toutes les ~10 secondes
- Le service ne change rien aux mises à jour de température

## 🔧 Ce que Fait le Service

Quand tu appelles `thermomaven.sync_devices` :

1. **Réinitialise le compteur** de tentatives automatiques (de 3 à 0)
2. **Appelle les endpoints API ThermoMaven** :
   - `/app/device/share/my/device/list`
   - `/app/device/share/shared/device/list`
3. **Déclenche l'envoi du message MQTT** `user:device:list` par le serveur
4. **Force le coordinator** à rafraîchir les données
5. **Crée les entités** dans Home Assistant pour les nouveaux thermomètres découverts

## 📊 Logs à Surveiller

Après avoir appelé le service, vérifie les logs :

```
Paramètres → Système → Logs
```

Tu devrais voir :
```
Manual device sync requested via service
Calling API endpoints to trigger MQTT device list...
Device sync triggered successfully
MQTT device list: X devices found
Adding Y new entities
```

## ⚙️ Comportement Normal vs. Problème

### ✅ Comportement Normal

```
Manual device sync requested via service
Triggering device list synchronization via API
Device sync triggered successfully
MQTT device list: 1 devices found
Adding 3 new entities
```
→ **Le service a fonctionné !** Les thermomètres sont découverts.

### ⚠️ Problème Potentiel

```
Manual device sync requested via service
Triggering device list synchronization via API
Device sync triggered successfully
MQTT device list: 0 devices found
```
→ **Aucun thermomètre trouvé**. Vérifie que :
- Ton thermomètre est allumé
- Il est connecté au WiFi (même réseau que HA si possible)
- Tu peux le voir dans l'application mobile ThermoMaven

## 💡 Astuces

### Automation de Récupération

Tu peux créer une automation qui appelle le service si aucun thermomètre n'est détecté :

```yaml
automation:
  - alias: "Auto-sync ThermoMaven si offline"
    trigger:
      - platform: state
        entity_id: sensor.mon_thermomaven_probe_1
        to: "unavailable"
        for: "00:05:00"  # Offline pendant 5 minutes
    action:
      - service: thermomaven.sync_devices
      - delay: "00:00:10"
      - service: notify.mobile_app
        data:
          message: "ThermoMaven: Synchronisation forcée"
```

### Dashboard Button

Ajoute un bouton dans ton dashboard pour appeler facilement le service :

```yaml
type: button
name: 🔄 Sync ThermoMaven
tap_action:
  action: call-service
  service: thermomaven.sync_devices
```

## 🆘 Support

Si le service ne fonctionne pas :
1. Vérifie les logs de Home Assistant
2. Assure-toi que l'intégration ThermoMaven est bien configurée
3. Teste avec l'application mobile ThermoMaven pour confirmer que tes thermomètres sont en ligne
4. Crée un issue sur GitHub avec les logs

---

**Note** : Ce service fait partie de la version 1.1.2+ de l'intégration ThermoMaven.

