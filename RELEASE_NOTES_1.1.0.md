# 🎉 ThermoMaven v1.1.0 - Real-Time MQTT Integration

## 🎊 Major Milestone: Fully Functional Integration!

We're excited to announce **v1.1.0**, the first **production-ready** release of the ThermoMaven Home Assistant integration! This version brings real-time temperature monitoring, automatic device discovery, and rock-solid reliability.

---

## 🚀 What's New

### ⚡ Real-Time Temperature Updates
- **~10 second updates** via MQTT push notifications
- **Zero polling overhead** - server pushes updates automatically
- **Instant notifications** when temperatures change

### 🎨 Automatic Device Discovery
- Devices appear **automatically** when powered on
- **No restart required** - entities created on-the-fly
- **Smart duplicate prevention**

### 🌡️ Accurate Temperature Readings
- **Fixed temperature conversion**: Now correctly converts °F → °C
- **Example**: Your thermometer shows 74.8°F → HA displays 23.8°C ✅

### 💾 Smart Caching
- **Resilient to API failures** - uses cached device data
- **Stable entities** - devices don't disappear during temporary issues
- **Seamless experience** - always shows your devices

### 🎨 Visual Polish
- **Custom icon** for better integration appearance
- **Professional branding** in Home Assistant UI

---

## 📊 Performance Improvements

| Feature | Before v1.1.0 | After v1.1.0 |
|---------|---------------|--------------|
| Temperature updates | Every 60-180s | Every ~10s ⚡ |
| HTTP requests | 60/hour | 12/hour |
| Device discovery | Manual restart | Automatic |
| Temperature accuracy | ❌ Wrong | ✅ Correct |
| Entity stability | ⚠️ Unstable | ✅ Stable |

---

## 🐛 Bug Fixes

- ✅ **Temperature conversion**: Fixed °F/10 → °C calculation
- ✅ **Entity creation**: Devices now appear automatically via MQTT
- ✅ **Device persistence**: Fixed disappearing devices when API is empty
- ✅ **MQTT topics**: Now subscribes to device-specific topics for real-time updates
- ✅ **Data loss**: Fixed coordinator losing device data on status updates

---

## 🎯 Supported Devices

All ThermoMaven wireless thermometers are supported:

| Model | Name | Probes | Status |
|-------|------|--------|--------|
| WT02 | ThermoMaven P2 | 2 | ✅ Tested |
| WT06 | ThermoMaven P4 | 4 | ✅ Tested |
| WT07 | ThermoMaven G2 | 2 | ✅ Tested |
| WT09 | ThermoMaven G4 | 4 | ✅ Tested |
| WT10 | ThermoMaven G1 | 1 | ✅ Tested |
| WT11 | ThermoMaven P1 | 1 | ✅ Tested |

---

## 📦 Installation

### New Installation

1. **Download** the latest release
2. **Copy** `custom_components/thermomaven` to your Home Assistant config folder
3. **Restart** Home Assistant
4. **Add Integration**: Settings → Devices & Services → Add Integration → ThermoMaven
5. **Enter credentials** and enjoy!

### Upgrade from Previous Version

1. **Backup** your current installation (optional but recommended)
2. **Replace** the `custom_components/thermomaven` folder
3. **Restart** Home Assistant
4. Your devices will appear automatically! 🎉

---

## 🎓 Quick Start

### Lovelace Card Example

```yaml
type: entities
title: 🔥 BBQ Monitor
entities:
  - entity: sensor.thermomaven_g1_probe_1
    name: Grill Temperature
    icon: mdi:thermometer
  - entity: sensor.thermomaven_g1_battery
    name: Battery
    icon: mdi:battery
```

### Automation Example

```yaml
automation:
  - alias: "🍖 Steak Ready"
    trigger:
      platform: numeric_state
      entity_id: sensor.thermomaven_g1_probe_1
      above: 60
    action:
      service: notify.mobile_app
      data:
        message: "Steak is ready! 🍖"
```

---

## 🔧 Technical Details

### Architecture
- **MQTT Push**: AWS IoT Core for real-time updates
- **REST API**: Backup polling every 5 minutes
- **Smart Caching**: Local device data persistence
- **Dynamic Entities**: Created automatically when devices appear

### Requirements
- Home Assistant 2023.1.0+
- Python 3.8+
- Internet connection for MQTT

---

## 📚 Documentation

- **[Installation Guide](HOMEASSISTANT_INSTALLATION.md)** - Detailed setup instructions
- **[README](README.md)** - Complete documentation
- **[Integration Summary](INTEGRATION_SUMMARY.md)** - Technical overview
- **[Changelog](CHANGELOG.md)** - Full version history

---

## 🙏 Acknowledgments

Special thanks to:
- The Home Assistant community
- ThermoMaven for creating great hardware
- All beta testers who helped make this release possible

---

## 🐛 Known Issues

None! This release is stable and production-ready. 🎉

If you encounter any issues, please [open an issue](https://github.com/djiesr/thermomaven-ha/issues).

---

## 🔮 What's Next?

Future plans for v1.2.0:
- Historical data graphs
- Cooking presets integration
- Multi-language support
- Advanced automation triggers

---

## 💬 Support

- **GitHub Issues**: [Report bugs](https://github.com/djiesr/thermomaven-ha/issues)
- **Discussions**: [Ask questions](https://github.com/djiesr/thermomaven-ha/discussions)
- **Home Assistant Community**: [Forum thread](https://community.home-assistant.io/)

---

**Happy grilling! 🔥🍖**

*Made with ❤️ for the BBQ and cooking community*

