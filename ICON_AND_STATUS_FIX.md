# 🎨 Correctifs v1.1.1 - Icône et Statut

## 🐛 Problèmes corrigés

### 1. Logo qui n'apparaît pas
**Problème** : L'icône n'était pas visible dans Home Assistant

**Solution** :
- ✅ Ajouté `logo.png` (copie de `icon.png`)
- ✅ Ajouté `issue_tracker` dans `manifest.json`
- ✅ Home Assistant utilise différents noms selon le contexte

**Fichiers concernés** :
- `custom_components/thermomaven/icon.png` (pour HACS)
- `custom_components/thermomaven/logo.png` (pour l'interface HA)

### 2. "Indisponible" au lieu de "Déconnecté"
**Problème** : Quand le thermomètre est éteint, HA affiche "Indisponible"

**Solution** :
- ✅ Les entités restent "disponibles" même quand l'appareil est offline
- ✅ Affichage de `None` (vide) au lieu de "Indisponible"
- ✅ Ajout d'attributs supplémentaires pour voir le statut

**Changements** :
- `available` retourne toujours `True` si l'appareil existe
- `native_value` retourne `None` si l'appareil est offline
- Ajout de `extra_state_attributes` avec le statut détaillé

## 📊 Résultat

### Avant
```
Probe 1: Indisponible
Battery: Indisponible
```

### Après
```
Probe 1: — (avec attribut "status: Hors ligne")
Battery: — (avec attribut "status: Hors ligne")
```

## 🎯 Attributs supplémentaires

Chaque capteur affiche maintenant des attributs détaillés :

### Capteur de température
```yaml
status: "En ligne" / "Hors ligne" / "Inconnu"
connection: "wifi" / "bluetooth" / "unknown"
cooking_state: "cooking" / "idle"
probe_battery: 100
```

### Capteur de batterie
```yaml
status: "En ligne" / "Hors ligne" / "Inconnu"
battery_status: "normal" / "low"
connection: "wifi" / "bluetooth"
wifi_rssi: -41
```

## 📝 Comment voir les attributs

Dans Home Assistant :
1. Cliquez sur l'entité (Probe 1 ou Battery)
2. Allez dans l'onglet **"Attributs"**
3. Vous verrez le statut détaillé

## 🎨 Utilisation dans Lovelace

### Afficher le statut avec une carte

```yaml
type: entities
title: ThermoMaven G1
entities:
  - entity: sensor.thermomaven_g1_probe_1
    secondary_info: attribute
    attribute: status
  - entity: sensor.thermomaven_g1_battery
    secondary_info: attribute
    attribute: status
```

### Carte conditionnelle (afficher seulement si en ligne)

```yaml
type: conditional
conditions:
  - entity: sensor.thermomaven_g1_probe_1
    state_not: "unknown"
card:
  type: gauge
  entity: sensor.thermomaven_g1_probe_1
  min: 0
  max: 100
```

### Template pour afficher le statut

```yaml
type: markdown
content: >
  {% if states('sensor.thermomaven_g1_probe_1') == 'unknown' %}
    🔴 Thermomètre déconnecté
  {% else %}
    🟢 Thermomètre en ligne: {{ states('sensor.thermomaven_g1_probe_1') }}°C
  {% endif %}
```

## 🔧 Installation

1. **Copiez les fichiers mis à jour** :
   ```
   custom_components/thermomaven/logo.png
   custom_components/thermomaven/manifest.json
   custom_components/thermomaven/sensor.py
   custom_components/thermomaven/strings.json
   ```

2. **Redémarrez Home Assistant**

3. **Vérifiez** :
   - Le logo devrait apparaître dans Paramètres → Intégrations
   - Les entités affichent "—" au lieu de "Indisponible" quand offline
   - Les attributs sont visibles dans les détails de l'entité

## 🎉 Résultat final

Maintenant, quand votre thermomètre est éteint :
- ✅ Les entités restent visibles (pas "Indisponible")
- ✅ La valeur est vide (—) avec le statut dans les attributs
- ✅ Le logo s'affiche correctement
- ✅ Vous pouvez créer des automatisations basées sur le statut

---

**Version** : 1.1.1  
**Date** : 12 octobre 2025

