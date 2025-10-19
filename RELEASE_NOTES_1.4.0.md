# 🎉 ThermoMaven v1.4.0 - Climate Control Release Notes

**Release Date:** January 19, 2025

## 🎛️ What's New - Climate Control!

This release adds **full temperature control** capabilities to the ThermoMaven Home Assistant integration! You can now set target temperatures and control cooking sessions directly from Home Assistant.

### ✨ New Features

#### Climate Entities for Temperature Control

Each probe now has its own climate entity that allows you to:

- 🌡️ **View current and target temperature** in one entity
- 🎯 **Set target temperature** (32°F - 572°F / 0°C - 300°C)
- ▶️ **Start cooking** with your desired target temperature
- ⏹️ **Stop/pause cooking** sessions
- 🔄 **Monitor cooking state** with preset modes

**New Entities:**
```
climate.thermomaven_[device]_probe_1_control
climate.thermomaven_[device]_probe_2_control
climate.thermomaven_[device]_probe_3_control  # For 4-probe models
climate.thermomaven_[device]_probe_4_control  # For 4-probe models
```

#### Climate Control Capabilities

**HVAC Modes:**
- 🔥 **Heat** - Cooking in progress
- ⏸️ **Off** - Cooking stopped/paused
- 🔄 **Auto** - Resting state

**Preset Modes:**
- 🍳 **Cooking** - Active cooking session
- ✅ **Ready** - Target temperature reached
- 😴 **Resting** - Resting period
- 🍽️ **Remove** - Ready to serve

**Temperature Control:**
- Set target temperature with 1°F precision
- Range: 32°F to 572°F (0°C to 300°C)
- Real-time updates via MQTT
- Automatic synchronization with device

### 🔧 Technical Implementation

#### MQTT Command Support

The integration now sends MQTT commands to control your ThermoMaven device:

**Command Type:** `WT:probe:control`

**Cooking Actions:**
- `1` = Start cooking
- `2` = Stop/pause cooking  
- `3` = Modify settings (temperature)

**Temperature Format:**
- Values are in tenths of degrees Fahrenheit
- Example: 165°F is sent as `1650`

#### New API Methods

Added to `ThermoMavenAPI`:

```python
async def async_set_probe_temperature(device_id, device_type, probe_color, target_temperature)
async def async_start_cooking(device_id, device_type, probe_color, target_temperature)
async def async_stop_cooking(device_id, device_type, probe_color)
```

#### Smart Topic Detection

- Automatically detects device publish topics from MQTT device list
- Falls back to standard topic format if needed
- Topic format: `app/device/{deviceId}/pub`

### 🌍 Translations

Climate entity names are now available in all supported languages:

- 🇬🇧 English - "Probe 1 Control"
- 🇫🇷 French - "Contrôle Sonde 1"  
- 🇩🇪 German - "Sonde 1 Steuerung"
- 🇪🇸 Spanish - "Control Sonda 1"
- 🇮🇹 Italian - "Controllo Sonda 1"
- 🇳🇱 Dutch - "Sonde 1 Bediening"

### 📋 Usage Examples

#### Basic Temperature Control

Set target temperature to 165°F:
```yaml
service: climate.set_temperature
target:
  entity_id: climate.thermomaven_device_probe_1_control
data:
  temperature: 165
```

#### Start Cooking

Start cooking session:
```yaml
service: climate.turn_on
target:
  entity_id: climate.thermomaven_device_probe_1_control
```

#### Stop Cooking

Stop cooking session:
```yaml
service: climate.turn_off
target:
  entity_id: climate.thermomaven_device_probe_1_control
```

#### Automation Example

Notify when target temperature is reached:
```yaml
automation:
  - alias: "Steak Ready"
    trigger:
      - platform: state
        entity_id: climate.thermomaven_grill_probe_1_control
        attribute: hvac_action
        to: "idle"
    condition:
      - condition: state
        entity_id: climate.thermomaven_grill_probe_1_control
        attribute: preset_mode
        state: "ready"
    action:
      - service: notify.mobile_app
        data:
          message: "Your steak has reached target temperature!"
```

### 🔄 Upgrade Instructions

#### From v1.3.0

1. **Backup your configuration** (recommended)
2. **Copy the new files** to your `custom_components/thermomaven/` directory
3. **Restart Home Assistant**
4. Climate entities will appear automatically for each probe

No configuration changes needed! The climate entities are created automatically.

### 🐛 Known Issues

None reported for this release.

### 📝 Breaking Changes

None. This release is fully backward compatible with v1.3.0.

All existing sensor entities continue to work as before. The climate entities are purely additive.

### 🙏 Acknowledgments

Special thanks to the reverse engineering of the ThermoMaven Android app which revealed the MQTT command structure for temperature control!

### 📚 Documentation

- [README](README.md) - Updated with climate control information
- [CHANGELOG](CHANGELOG.md) - Full version history
- [API Documentation](api/) - MQTT protocol details

### 🔗 Links

- **GitHub Repository:** https://github.com/djiesr/thermomaven-ha
- **Issue Tracker:** https://github.com/djiesr/thermomaven-ha/issues
- **Home Assistant Community:** Coming soon!

---

## What's Next?

We're exploring:
- 📊 Multi-zone temperature control
- ⏰ Timer and alarm controls
- 📈 Temperature history graphs
- 🔔 Advanced notification options

Have suggestions? [Open an issue](https://github.com/djiesr/thermomaven-ha/issues)!

---

**Enjoy your new climate control features!** 🎉🌡️

