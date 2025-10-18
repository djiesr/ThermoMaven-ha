# Correctif de Découverte des Devices ThermoMaven

## Problème Identifié

L'intégration ThermoMaven ne détectait les thermomètres que lorsque l'application mobile était ouverte sur le téléphone. Après la détection initiale, tout fonctionnait correctement même en fermant l'application.

### Cause Racine

Le système ThermoMaven utilise une architecture hybride API REST + MQTT :

1. **MQTT** : Utilisé pour les mises à jour en temps réel (températures, statuts)
2. **API REST** : Utilisé pour déclencher certaines actions côté serveur

**Le problème** : Le message MQTT `user:device:list` (qui contient la liste des thermomètres) n'est publié par le broker MQTT que lorsqu'un client appelle les endpoints API de listing :
- `/app/device/share/my/device/list`
- `/app/device/share/shared/device/list`

L'application mobile ThermoMaven appelle automatiquement ces endpoints au démarrage, ce qui déclenche l'envoi du message MQTT. L'intégration Home Assistant, elle, se connectait au MQTT mais attendait passivement ce message sans jamais le déclencher.

## Solution Implémentée

L'intégration a été modifiée pour appeler activement les endpoints API et déclencher la synchronisation des devices :

### 1. Synchronisation à la Connexion MQTT

Quand l'intégration se connecte au broker MQTT, elle appelle maintenant automatiquement les endpoints API pour déclencher l'envoi du message `user:device:list`.

```python
def _on_mqtt_connect(self, client, userdata, flags, rc):
    if rc == 0:
        # Subscribe to topics
        for topic in self.mqtt_config["subTopics"]:
            client.subscribe(topic)
        
        # Trigger device list sync by calling API endpoints
        self.hass.add_job(self._trigger_device_sync())
```

### 2. Synchronisation Initiale après Setup MQTT

Une synchronisation supplémentaire est déclenchée après la configuration MQTT pour garantir que les devices soient découverts même s'il y a un problème de timing :

```python
async def async_setup_mqtt(self, coordinator):
    # ... setup MQTT ...
    
    # Trigger initial device sync after MQTT setup
    await asyncio.sleep(2)  # Give MQTT time to connect
    await self._trigger_device_sync()
```

### 3. Synchronisation de Secours dans le Coordinator

Si aucun device n'est découvert lors d'une mise à jour du coordinator, une nouvelle synchronisation est automatiquement déclenchée :

```python
async def _async_update_data(self):
    devices = await self.api.async_get_devices()
    
    # If no devices are returned and MQTT is connected, trigger a sync
    if not devices and self.api.mqtt_client and self.api.mqtt_client.is_connected():
        await self.api._trigger_device_sync()
```

### 4. Méthode de Synchronisation

La nouvelle méthode `_trigger_device_sync()` appelle les endpoints API qui déclenchent l'envoi du message MQTT :

```python
async def _trigger_device_sync(self):
    """Trigger device synchronization by calling API endpoints.
    
    This causes the MQTT broker to publish the user:device:list message,
    which is needed for device discovery.
    """
    await asyncio.sleep(1)  # Ensure MQTT subscription is active
    await self.async_get_devices()  # Calls both my/device/list and shared/device/list
```

## Fichiers Modifiés

- `github/custom_components/thermomaven/thermomaven_api.py`
  - Ajout de `_trigger_device_sync()` 
  - Modification de `_on_mqtt_connect()` pour déclencher la sync
  - Modification de `async_setup_mqtt()` pour sync initiale

- `github/custom_components/thermomaven/__init__.py`
  - Modification de `_async_update_data()` pour sync de secours

## Test de la Solution

Pour tester le correctif :

1. **Supprimer l'intégration** existante dans Home Assistant
2. **Redémarrer** Home Assistant
3. **Réinstaller** l'intégration ThermoMaven **SANS ouvrir l'application mobile**
4. **Attendre** environ 10-15 secondes

Les thermomètres devraient maintenant être détectés automatiquement sans avoir besoin d'ouvrir l'application mobile.

## Protection Anti-Spam API

Pour éviter de surcharger l'API ThermoMaven si aucun thermomètre n'est détecté, le système inclut des protections :

### Limite de Tentatives Automatiques
- **Maximum 3 tentatives** de synchronisation automatique après le setup
- Si aucun device n'est trouvé après 3 tentatives, les tentatives automatiques s'arrêtent
- Le compteur se réinitialise dès qu'un device est détecté

### Service Manuel
Un service Home Assistant est disponible pour forcer la synchronisation manuellement :

**Service** : `thermomaven.sync_devices`

**Comment l'utiliser** :
1. Ouvrir Outils de développement → Services
2. Chercher "ThermoMaven: Synchroniser les appareils"
3. Cliquer sur "Appeler le service"

Ou via une automation/script :
```yaml
service: thermomaven.sync_devices
```

**Quand l'utiliser** :
- Si tes thermomètres ne sont pas détectés après l'installation
- Après avoir allumé un nouveau thermomètre
- Si tu as atteint la limite de 3 tentatives automatiques

## Comportement Attendu

- ✅ Les devices sont découverts automatiquement au démarrage de Home Assistant
- ✅ Pas besoin d'ouvrir l'application mobile pour la découverte initiale
- ✅ Les mises à jour de température continuent de fonctionner via MQTT
- ✅ **Maximum 3 tentatives** automatiques si aucun device n'est trouvé (toutes les 5 minutes)
- ✅ Service manuel `thermomaven.sync_devices` disponible pour forcer la synchronisation

## Logs de Débogage

Si vous souhaitez vérifier le fonctionnement dans les logs de Home Assistant, recherchez :

```
Connected to MQTT broker
Triggering device list synchronization via API
Calling API endpoints to trigger MQTT device list...
Device sync triggered successfully
MQTT device list: X devices found
```

## Notes Techniques

Cette solution respecte l'architecture du système ThermoMaven où :
- L'API REST sert de "déclencheur" pour certaines actions
- Le MQTT sert de canal de distribution des données en temps réel
- Les clients doivent activement "demander" certaines informations via l'API REST pour que le serveur les publie sur MQTT

Cette approche est similaire à celle utilisée par l'application mobile officielle.

