# ThermoMaven Home Assistant Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-orange)](https://www.home-assistant.io/)
[![Version](https://img.shields.io/badge/Version-1.4.4-blue)](https://github.com/djiesr/thermomaven-ha)
[![hacs](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

Intégration Home Assistant pour les thermomètres sans fil ThermoMaven (P1, P2, P4, G1, G2, G4).

## ✨ Fonctionnalités

- 🌡️ **Surveillance de température en temps réel** via MQTT
- 📊 **17+ capteurs par appareil** (température, batterie, cuisson, WiFi)
- 🎛️ **Contrôle de température** avec entités Climate (v1.4.0+)
- ⏱️ **Suivi du temps de cuisson** (total, actuel, restant)
- 🔋 **Niveau de batterie** (appareil et sondes)
- 📡 **Signal WiFi** (RSSI)
- 🌍 **Multi-langue** (EN, FR, ES, PT, DE, ZH)
- 🔄 **Mises à jour automatiques** via MQTT push

## 📱 Appareils Supportés

| Modèle | Nom | Sondes | Description |
|--------|-----|--------|-------------|
| **WT02** | ThermoMaven P2 | 2 | Thermomètre professionnel 2 sondes |
| **WT06** | ThermoMaven P4 | 4 | Thermomètre professionnel 4 sondes |
| **WT07** | ThermoMaven G2 | 2 | Thermomètre grill 2 sondes |
| **WT09** | ThermoMaven G4 | 4 | Thermomètre grill 4 sondes |
| **WT10** | ThermoMaven G1 | 1 | Thermomètre grill 1 sonde |
| **WT11** | ThermoMaven P1 | 1 | Thermomètre professionnel 1 sonde |

## 📦 Installation

### Option 1 : Installation via HACS (Recommandé)

1. **Ouvrez HACS** dans Home Assistant
2. Allez dans **Intégrations**
3. Cliquez sur **⋮** (menu) → **Dépôts personnalisés**
4. Ajoutez l'URL : `https://github.com/djiesr/thermomaven-ha`
5. Catégorie : **Intégration**
6. Cliquez sur **Ajouter**
7. Cherchez **"ThermoMaven"** dans HACS
8. Cliquez sur **Télécharger**
9. **Redémarrez Home Assistant**

### Option 2 : Installation Manuelle

1. **Téléchargez** la [dernière version](https://github.com/djiesr/thermomaven-ha/releases/latest)
2. **Extrayez** le dossier `custom_components/thermomaven`
3. **Copiez** le dossier dans : `/config/custom_components/thermomaven/`
4. **Redémarrez Home Assistant**

Structure finale :
```
config/
└── custom_components/
    └── thermomaven/
        ├── __init__.py
        ├── manifest.json
        ├── config_flow.py
        ├── sensor.py
        ├── climate.py
        ├── thermomaven_api.py
        ├── const.py
        └── translations/
```

## ⚙️ Configuration

### 1. Ajouter l'Intégration

Après l'installation et le redémarrage :

1. Allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur **+ Ajouter une intégration**
3. Cherchez **"ThermoMaven"**
4. Cliquez sur l'intégration ThermoMaven

### 2. Entrez vos Identifiants

<img src="https://via.placeholder.com/600x300/1f1f1f/ffffff?text=Configuration+ThermoMaven" alt="Configuration" width="500"/>

Renseignez :
- **Email** : Votre email ThermoMaven
- **Mot de passe** : Votre mot de passe ThermoMaven
- **Région** : Sélectionnez votre pays/région

**Note :** Ce sont les mêmes identifiants que l'application mobile ThermoMaven.

### 3. Validation

L'intégration va :
- ✅ Se connecter à l'API ThermoMaven
- ✅ Établir la connexion MQTT pour les mises à jour en temps réel
- ✅ Découvrir automatiquement vos appareils
- ✅ Créer toutes les entités (capteurs et contrôles)

## 🎯 Résultat dans Home Assistant

### 📊 Entités Créées Automatiquement

Pour **chaque appareil ThermoMaven**, vous obtiendrez :

#### 🌡️ Capteurs de Température (par sonde)

```
sensor.thermomaven_[appareil]_probe_1          # Température sonde 1
sensor.thermomaven_[appareil]_probe_2          # Température sonde 2
sensor.thermomaven_[appareil]_probe_3          # Température sonde 3 (si disponible)
sensor.thermomaven_[appareil]_probe_4          # Température sonde 4 (si disponible)
```

#### 🔥 Capteurs de Zones (pour chaque sonde)

```
sensor.thermomaven_[appareil]_area_1_tip       # Zone 1 (Pointe)
sensor.thermomaven_[appareil]_area_2           # Zone 2
sensor.thermomaven_[appareil]_area_3           # Zone 3
sensor.thermomaven_[appareil]_area_4           # Zone 4
sensor.thermomaven_[appareil]_area_5_handle    # Zone 5 (Poignée)
```

#### 🎛️ Contrôles Climate (v1.4.0+) ✨

```
climate.thermomaven_[appareil]_probe_1_control # Contrôle sonde 1
climate.thermomaven_[appareil]_probe_2_control # Contrôle sonde 2
climate.thermomaven_[appareil]_probe_3_control # Contrôle sonde 3 (si disponible)
climate.thermomaven_[appareil]_probe_4_control # Contrôle sonde 4 (si disponible)
```

**Fonctionnalités Climate :**
- 🎯 Définir température cible (32-572°F / 0-300°C)
- ▶️ Démarrer/arrêter la cuisson
- 📊 Afficher température actuelle et cible
- 🔄 Modes : Off, Heat, Auto
- 📋 Presets : Cooking, Ready, Resting, Remove

#### ⏱️ Capteurs de Cuisson

```
sensor.thermomaven_[appareil]_total_cook_time     # Temps total
sensor.thermomaven_[appareil]_current_cook_time   # Temps actuel
sensor.thermomaven_[appareil]_remaining_cook_time # Temps restant
sensor.thermomaven_[appareil]_cooking_mode        # Mode de cuisson
sensor.thermomaven_[appareil]_cooking_state       # État actuel
```

#### 🔋 Capteurs Batterie & WiFi

```
sensor.thermomaven_[appareil]_battery          # Batterie appareil
sensor.thermomaven_[appareil]_probe_battery    # Batterie sonde
sensor.thermomaven_[appareil]_wifi_signal      # Signal WiFi (RSSI)
```

#### 🌡️ Capteurs Environnement

```
sensor.thermomaven_[appareil]_ambient          # Température ambiante
sensor.thermomaven_[appareil]_target           # Température cible
```

### 📱 Exemple d'Interface

Vos appareils apparaîtront dans :
- **Paramètres** → **Appareils et services** → **ThermoMaven**
- **Aperçu** (pour créer des cartes)
- **Outils de développement** → **États**

<img src="https://via.placeholder.com/800x400/1f1f1f/ffffff?text=Entités+ThermoMaven+dans+Home+Assistant" alt="Entités" width="700"/>

## 💡 Exemples d'Utilisation

### Carte Thermostat

```yaml
type: thermostat
entity: climate.thermomaven_grill_probe_1_control
name: Steak
features:
  - type: climate-hvac-modes
    hvac_modes:
      - "off"
      - heat
```

### Carte de Surveillance

```yaml
type: entities
title: 🔥 BBQ Monitor
entities:
  - entity: sensor.thermomaven_grill_probe_1
    name: Steak
    icon: mdi:food-steak
  - entity: sensor.thermomaven_grill_probe_2
    name: Poulet
    icon: mdi:food-drumstick
  - entity: sensor.thermomaven_grill_battery
    name: Batterie
  - entity: sensor.thermomaven_grill_wifi_signal
    name: WiFi
```

### Graphique Historique

```yaml
type: history-graph
title: Température - 3 dernières heures
entities:
  - sensor.thermomaven_grill_probe_1
  - sensor.thermomaven_grill_probe_2
hours_to_show: 3
```

### Automation : Alerte de Cuisson

```yaml
automation:
  - alias: "🍖 Steak Prêt"
    trigger:
      - platform: numeric_state
      entity_id: sensor.thermomaven_grill_probe_1
      above: 60  # 60°C
    action:
      - service: notify.mobile_app
        data:
          title: "🍖 BBQ"
          message: "Le steak est prêt ! ({{ states('sensor.thermomaven_grill_probe_1') }}°C)"
```

### Automation : Batterie Faible

```yaml
automation:
  - alias: "🔋 Batterie Faible"
    trigger:
      - platform: numeric_state
      entity_id: sensor.thermomaven_grill_battery
      below: 20
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Batterie Faible"
          message: "ThermoMaven : {{ states('sensor.thermomaven_grill_battery') }}%"
```

## 🔧 Dépannage

### Les Capteurs Sont "Non Disponible"

**✅ Solution :**
1. Vérifiez que vos appareils ThermoMaven sont allumés
2. Vérifiez qu'ils sont connectés au WiFi
3. Rechargez l'intégration : **Paramètres** → **Intégrations** → **ThermoMaven** → **⋮** → **Recharger**

### Aucun Appareil Détecté

**✅ Vérifications :**
- Les appareils sont bien associés à votre compte dans l'app mobile
- Les appareils sont sous tension et connectés au WiFi
- Vos identifiants ThermoMaven sont corrects

### Problème de Connexion MQTT

**✅ Vérifications :**
- Votre connexion Internet fonctionne
- Le port 8883 n'est pas bloqué par votre pare-feu
- Consultez les logs : **Paramètres** → **Système** → **Journaux**

### Les Entités Climate Ne S'Affichent Pas

**✅ Solution (v1.4.0+) :**
1. Vérifiez que vous avez bien la version 1.4.0+
2. Redémarrez Home Assistant complètement
3. Les entités climate apparaissent automatiquement après redémarrage

### Activer les Logs de Debug

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.thermomaven: debug
```

Puis : **Paramètres** → **Système** → **Journaux** et filtrez par "thermomaven"

## 🚧 À Faire (Roadmap)

Fonctionnalités prévues pour les prochaines versions :

### 🎯 Version 1.5.0 (Planifiée)

- **Synchronisation Target Temperature**
  - Modifier le capteur `sensor.thermomaven_*_target_temperature` depuis l'entité Climate
  - Synchronisation bidirectionnelle entre sensor et climate
  
- **Contrôle du Cook Time**
  - Définir une durée de cuisson cible
  - Alarmes et notifications quand le temps est écoulé
  - Gestion du temps restant
  
- **Gestion avancée du Cooking Mode**
  - Sélection du mode de cuisson (Smart, Manual, etc.)
  - Presets de cuisson personnalisés
  - Profils de température par type d'aliment

### 🔮 Futures Améliorations

- 📊 Graphiques d'historique de température
- 📱 Notifications push avancées
- 🎨 Presets de cuisson personnalisables
- ⏰ Minuteries et alarmes multiples
- 🌡️ Gestion multi-zones améliorée

**Contributions bienvenues !** Si vous souhaitez implémenter une de ces fonctionnalités, ouvrez une issue ou pull request.

## 📚 Documentation Complète

- **[Guide Contrôle Climate](CLIMATE_CONTROL_GUIDE.md)** - Utilisation des entités Climate
- **[Notes de Version 1.4.4](RELEASE_NOTES_1.4.4.md)** - Dernières nouveautés
- **[Changelog](CHANGELOG.md)** - Historique des versions
- **[Architecture Technique](ARCHITECTURE.md)** - Détails techniques

## 🆕 Nouveautés v1.4.4

### 🎛️ Contrôle Climate
- Entités Climate pour contrôle de température
- Définir température cible (32-572°F / 0-300°C)
- Démarrer/arrêter cuisson
- Modes HVAC et Presets

### 🐛 Corrections Critiques
- ✅ Température cible persiste correctement
- ⚡ API flooding arrêté (95% réduction appels)
- 📡 Détection MQTT topic fixée (WT10, WT02, etc.)

### 📊 Fonctionnalités Complètes
- **17+ capteurs** par appareil
- **Mises à jour temps réel** via MQTT
- **Multi-langue** (6 langues)
- **Performance optimisée**

## ⚠️ Prérequis

- **Home Assistant** 2023.1.0 ou supérieur
- **Compte ThermoMaven** avec au moins un appareil associé
- **Connexion Internet** (pour MQTT)

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

## ⚠️ Avertissement

Ceci est une intégration **non officielle** créée par reverse engineering de l'application mobile officielle. Non affilié à ThermoMaven.

**Utilisez à vos propres risques.**

## 🤝 Contribuer

Les contributions sont bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements
4. Push vers la branche
5. Ouvrez une Pull Request

## 📞 Support

- 🐛 **Bugs** : [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- 📖 **Wiki** : [Documentation Wiki](https://github.com/djiesr/thermomaven-ha/wiki)

---

**🔥 Fait avec ❤️ pour la communauté BBQ et culinaire**

*Bon appétit ! 🍖🔥*
