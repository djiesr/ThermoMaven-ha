# ThermoMaven Home Assistant Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-orange)](https://www.home-assistant.io/)
[![Version](https://img.shields.io/badge/Version-1.4.5-blue)](https://github.com/djiesr/thermomaven-ha)
[![hacs](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

Home Assistant integration for ThermoMaven wireless thermometers (P1, P2, P4, G1, G2, G4).

## ✨ Features

- 🌡️ **Real-time temperature monitoring** via MQTT
- 📊 **17+ sensors per device** (temperature, battery, cooking time, WiFi)
- 🎛️ **Temperature control** with Climate entities (v1.4.0+)
- ⏱️ **Cooking time tracking** (total, current, remaining)
- 🔋 **Battery levels** (device and probes)
- 📡 **WiFi signal** (RSSI)
- 🌍 **Multi-language** (EN, FR, ES, PT, DE, ZH)
- 🔄 **Automatic updates** via MQTT push

## 📱 Supported Devices

| Model | Name | Probes | Description |
|-------|------|--------|-------------|
| **WT02** | ThermoMaven P2 | 2 | Professional 2-probe thermometer |
| **WT06** | ThermoMaven P4 | 4 | Professional 4-probe thermometer |
| **WT07** | ThermoMaven G2 | 2 | Grill 2-probe thermometer |
| **WT09** | ThermoMaven G4 | 4 | Grill 4-probe thermometer |
| **WT10** | ThermoMaven G1 | 1 | Single-probe grill thermometer |
| **WT11** | ThermoMaven P1 | 1 | Single-probe professional thermometer |

## 📦 Installation

### Option 1: Installation via HACS (Recommended)

1. **Open HACS** in Home Assistant
2. Go to **Integrations**
3. Click **⋮** (menu) → **Custom repositories**
4. Add URL: `https://github.com/djiesr/thermomaven-ha`
5. Category: **Integration**
6. Click **Add**
7. Search for **"ThermoMaven"** in HACS
8. Click **Download**
9. **Restart Home Assistant**

### Option 2: Manual Installation

1. **Download** the [latest release](https://github.com/djiesr/thermomaven-ha/releases/latest)
2. **Extract** the `custom_components/thermomaven` folder
3. **Copy** to: `/config/custom_components/thermomaven/`
4. **Restart Home Assistant**

Final structure:
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

### 1. Add the Integration

After installation and restart:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"ThermoMaven"**
4. Click on ThermoMaven integration

### 2. Enter Your Credentials

Enter:
- **Email**: Your ThermoMaven email
- **Password**: Your ThermoMaven password
- **Region**: Select your country/region

**Note:** Use the same credentials as the ThermoMaven mobile app.

### 3. Validation

The integration will:
- ✅ Connect to ThermoMaven API
- ✅ Establish MQTT connection for real-time updates
- ✅ Auto-discover your devices
- ✅ Create all entities (sensors and controls)

## 🎯 Entities Created in Home Assistant

### 📊 Automatically Created Entities

For **each ThermoMaven device**, you'll get:

#### 🌡️ Temperature Sensors (per probe)

```
sensor.thermomaven_[device]_probe_1          # Probe 1 temperature
sensor.thermomaven_[device]_probe_2          # Probe 2 temperature
sensor.thermomaven_[device]_probe_3          # Probe 3 temperature (if available)
sensor.thermomaven_[device]_probe_4          # Probe 4 temperature (if available)
```

#### 🔥 Zone Sensors (for each probe)

```
sensor.thermomaven_[device]_area_1_tip       # Zone 1 (Tip)
sensor.thermomaven_[device]_area_2           # Zone 2
sensor.thermomaven_[device]_area_3           # Zone 3
sensor.thermomaven_[device]_area_4           # Zone 4
sensor.thermomaven_[device]_area_5_handle    # Zone 5 (Handle)
```

#### 🎛️ Climate Controls (v1.4.0+) ✨

```
climate.thermomaven_[device]_probe_1_control # Probe 1 control
climate.thermomaven_[device]_probe_2_control # Probe 2 control
climate.thermomaven_[device]_probe_3_control # Probe 3 control (if available)
climate.thermomaven_[device]_probe_4_control # Probe 4 control (if available)
```

**Climate Features:**
- 🎯 Set target temperature (32-572°F / 0-300°C)
- ▶️ Start/stop cooking
- 📊 Display current and target temperature
- 🔄 Modes: Off, Heat, Auto
- 📋 Presets: Cooking, Ready, Resting, Remove

#### ⏱️ Cooking Sensors

```
sensor.thermomaven_[device]_total_cook_time     # Total time
sensor.thermomaven_[device]_current_cook_time   # Current time
sensor.thermomaven_[device]_remaining_cook_time # Remaining time
sensor.thermomaven_[device]_cooking_mode        # Cooking mode
sensor.thermomaven_[device]_cooking_state       # Current state
```

#### 🔋 Battery & WiFi Sensors

```
sensor.thermomaven_[device]_battery          # Device battery
sensor.thermomaven_[device]_probe_battery    # Probe battery
sensor.thermomaven_[device]_wifi_signal      # WiFi signal (RSSI)
```

#### 🌡️ Environment Sensors

```
sensor.thermomaven_[device]_ambient          # Ambient temperature
sensor.thermomaven_[device]_target           # Target temperature
```

## 💡 Usage Examples

### Thermostat Card

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

### Monitoring Card

```yaml
type: entities
title: 🔥 BBQ Monitor
entities:
  - entity: sensor.thermomaven_grill_probe_1
    name: Steak
    icon: mdi:food-steak
  - entity: sensor.thermomaven_grill_probe_2
    name: Chicken
    icon: mdi:food-drumstick
  - entity: sensor.thermomaven_grill_battery
    name: Battery
  - entity: sensor.thermomaven_grill_wifi_signal
    name: WiFi
```

### History Graph

```yaml
type: history-graph
title: Temperature - Last 3 Hours
entities:
  - sensor.thermomaven_grill_probe_1
  - sensor.thermomaven_grill_probe_2
hours_to_show: 3
```

### Automation: Cooking Alert

```yaml
automation:
  - alias: "🍖 Steak Ready"
    trigger:
      - platform: numeric_state
        entity_id: sensor.thermomaven_grill_probe_1
        above: 60  # 60°C
    action:
      - service: notify.mobile_app
        data:
          title: "🍖 BBQ"
          message: "Steak is ready! ({{ states('sensor.thermomaven_grill_probe_1') }}°C)"
```

### Automation: Low Battery

```yaml
automation:
  - alias: "🔋 Low Battery"
    trigger:
      - platform: numeric_state
        entity_id: sensor.thermomaven_grill_battery
        below: 20
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Low Battery"
          message: "ThermoMaven: {{ states('sensor.thermomaven_grill_battery') }}%"
```

## 🔧 Troubleshooting

### Sensors Show "Unavailable"

**✅ Solution:**
1. Check that your ThermoMaven devices are powered on
2. Check WiFi connection
3. Reload integration: **Settings** → **Integrations** → **ThermoMaven** → **⋮** → **Reload**

### No Devices Detected

**✅ Checks:**
- Devices are paired with your account in the mobile app
- Devices are powered on and connected to WiFi
- Your ThermoMaven credentials are correct
- Are you set the same country of your app

### MQTT Connection Issues

**✅ Checks:**
- Internet connection is working
- Port 8883 is not blocked by firewall
- Check logs: **Settings** → **System** → **Logs**

### Climate Entities Not Showing

**✅ Solution (v1.4.0+):**
1. Verify you have version 1.4.0+
2. Completely restart Home Assistant
3. Climate entities appear automatically after restart

### Enable Debug Logs

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.thermomaven: debug
```

Then: **Settings** → **System** → **Logs** and filter by "thermomaven"

## 🚧 Roadmap (To Do)

Planned features for upcoming versions:

### 🎯 Version 1.5.0 (Planned)

- **Target Temperature Synchronization**
  - Update `sensor.thermomaven_*_target_temperature` from Climate entity
  - Bidirectional sync between sensor ↔ climate
  
- **Cook Time Control**
  - Set target cooking duration
  - Alarms and notifications when time elapsed
  - Remaining time management
  
- **Advanced Cooking Mode Management**
  - Select cooking mode (Smart, Manual, etc.)
  - Custom cooking presets
  - Temperature profiles by food type

### 🔮 Future Improvements

- 📊 Temperature history graphs
- 📱 Advanced push notifications
- 🎨 Customizable cooking presets
- ⏰ Multiple timers and alarms
- 🌡️ Enhanced multi-zone management

**Contributions welcome!** If you'd like to implement any of these features, open an issue or pull request.

## 📚 Complete Documentation

- **[Climate Control Guide](CLIMATE_CONTROL_GUIDE.md)** - Using Climate entities
- **[Release Notes 1.4.4](RELEASE_NOTES_1.4.4.md)** - Latest updates
- **[Changelog](CHANGELOG.md)** - Version history
- **[Technical Architecture](ARCHITECTURE.md)** - Technical details

## 🆕 What's New in v1.4.5

### 🎛️ Climate Control
- Climate entities for temperature control
- Set target temperature (32-572°F / 0-300°C)
- Start/stop cooking
- HVAC modes and Presets

### 🐛 Critical Fixes
- ✅ Target temperature persists correctly
- ⚡ API flooding stopped (95% reduction)
- 📡 MQTT topic detection fixed (WT10, WT02, etc.)

### 📊 Complete Features
- **17+ sensors** per device
- **Real-time updates** via MQTT
- **Multi-language** (6 languages)
- **Optimized performance**

## ⚠️ Requirements

- **Home Assistant** 2023.1.0 or higher
- **ThermoMaven account** with at least one paired device
- **Internet connection** (for MQTT)

## 📝 License

MIT License - See [LICENSE](LICENSE)

## ⚠️ Disclaimer

This is an **unofficial integration** created by reverse engineering the official mobile app. Not affiliated with ThermoMaven.

**Use at your own risk.**

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a branch (`git checkout -b feature/new-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

- 🐛 **Bugs**: [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- 📖 **Wiki**: [Documentation Wiki](https://github.com/djiesr/thermomaven-ha/wiki)

---

**🔥 Made with ❤️ for the BBQ and cooking community**

*Happy grilling! 🍖🔥*
