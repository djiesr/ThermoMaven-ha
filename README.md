# ThermoMaven Home Assistant Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-orange)](https://www.home-assistant.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-1.3.0-blue)](https://github.com/yourusername/thermomaven-homeassistant)

A comprehensive Home Assistant integration and Python client for ThermoMaven wireless thermometers, reverse-engineered from the official mobile app.

## 🎯 Features

### ✅ Core Functionality
- **Complete REST API client** with MD5 signature authentication
- **Real-time MQTT communication** via AWS IoT Core
- **Home Assistant integration** with custom component
- **Automatic device discovery** and entity creation
- **17+ sensors per device** (temperature, battery, cooking time, WiFi, etc.)
- **Multi-language support** (English, French, Spanish, Portuguese, German, Chinese)
- **Smart API caching** (reduces API calls by 98%)
- **Multiple device support** (P1, P2, P4, G1, G2, G4)

### 🌡️ Advanced Temperature Monitoring
- **Real-time temperature updates** via MQTT push
- **5 area temperature sensors** (Tip → Handle zones)
- **Ambient & target temperature** tracking
- **Accurate temperature conversion** (Fahrenheit → Celsius)
- **Multi-probe monitoring** (up to 4 probes per device)
- **Temperature history** and graphing
- **Custom temperature alerts** and notifications

### ⏱️ Cooking Features (NEW in v1.3.0)
- **Cooking time tracking** (total, current, remaining)
- **Cooking mode monitoring** (smart, manual, etc.)
- **Cooking state tracking** (cooking, idle, standby, charging)
- **Target temperature alerts**

## 📱 Supported Devices

| Model | Name | Probes | Description |
|-------|------|--------|-------------|
| **WT02** | ThermoMaven P2 | 2 | Professional dual-probe thermometer |
| **WT06** | ThermoMaven P4 | 4 | Professional quad-probe thermometer |
| **WT07** | ThermoMaven G2 | 2 | Grill dual-probe thermometer |
| **WT09** | ThermoMaven G4 | 4 | Grill quad-probe thermometer |
| **WT10** | ThermoMaven G1 | 1 | Single-probe grill thermometer |
| **WT11** | ThermoMaven P1 | 1 | Single-probe professional thermometer |

## 🚀 Quick Start

### 🐍 Python Client

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure credentials:**
```bash
cp env.example .env
# Edit .env with your ThermoMaven credentials
```

3. **Run the client:**
```bash
python thermomaven_client.py
```

### 📡 MQTT Client (Real-time)

For real-time temperature monitoring:

```bash
python thermomaven_mqtt_client.py
```

### 🏠 Home Assistant Integration

#### Prerequisites
- Home Assistant Core 2023.1 or higher
- ThermoMaven account with at least one paired device

#### Installation

1. **Copy the integration:**
   ```bash
   # Copy custom_components/thermomaven to your HA config folder
   cp -r custom_components/thermomaven /config/custom_components/
   ```

2. **Restart Home Assistant:**
   ```
   Settings → System → Restart
   ```

3. **Add the integration:**
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for **"ThermoMaven"**
   - Enter your ThermoMaven credentials (email/password)
   - Click **Submit**

4. **Your devices will appear automatically!** 🎉

#### What you'll get:

For each ThermoMaven device, **17 sensors** are created automatically:

**🌡️ Temperature Sensors:**
```
sensor.thermomaven_[device]_area_1_tip       # Zone 1 (Tip)
sensor.thermomaven_[device]_area_2           # Zone 2
sensor.thermomaven_[device]_area_3           # Zone 3
sensor.thermomaven_[device]_area_4           # Zone 4
sensor.thermomaven_[device]_area_5_handle    # Zone 5 (Handle)
sensor.thermomaven_[device]_ambient          # Ambient Temperature
sensor.thermomaven_[device]_target           # Target Temperature
```

**⏱️ Cooking Sensors:**
```
sensor.thermomaven_[device]_total_cook_time     # Total cooking time
sensor.thermomaven_[device]_current_cook_time   # Current session time
sensor.thermomaven_[device]_remaining_cook_time # Time remaining
sensor.thermomaven_[device]_cooking_mode        # Cooking mode
sensor.thermomaven_[device]_cooking_state       # Current state
```

**🔋 Battery & Connectivity:**
```
sensor.thermomaven_[device]_battery          # Device battery
sensor.thermomaven_[device]_probe_battery    # Probe battery
sensor.thermomaven_[device]_wifi_signal      # WiFi signal (RSSI)
```

## 📚 Documentation

- **[Home Assistant Installation](HOMEASSISTANT_INSTALLATION.md)** - Detailed HA setup guide
- **[Architecture](ARCHITECTURE.md)** - Technical architecture and data flow
- **[Changelog](CHANGELOG.md)** - Version history and release notes
- **[API Documentation](api/)** - REST API and MQTT guides
- **[Translations Guide](custom_components/thermomaven/translations/README.md)** - Multi-language support

## 🔧 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Home Assistant                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │         ThermoMaven Integration (v1.3.0)           │ │
│  │                                                     │ │
│  │  ┌──────────────┐        ┌──────────────────┐     │ │
│  │  │   REST API   │        │   MQTT Client    │     │ │
│  │  │  (Login &    │───────▶│  (Real-time      │     │ │
│  │  │   Devices)   │        │   Updates)       │     │ │
│  │  └──────┬───────┘        └────────┬─────────┘     │ │
│  │         │                         │               │ │
│  │         └────────┬────────────────┘               │ │
│  │                  ▼                                │ │
│  │         ┌────────────────┐                        │ │
│  │         │  Coordinator   │                        │ │
│  │         │  + Cache       │                        │ │
│  │         │  (Data Merge)  │                        │ │
│  │         └────────┬───────┘                        │ │
│  │                  │                                │ │
│  │         ┌────────▼────────┐                       │ │
│  │         │   17 Sensors    │                       │ │
│  │         │   per Device    │                       │ │
│  │         └─────────────────┘                       │ │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
      ┌───────────────────────────────┐
      │   ThermoMaven Cloud API       │
      │   + AWS IoT Core (MQTT)       │
      └───────────────────────────────┘
```

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for detailed technical documentation.

## 📊 Example Usage

### 🐍 Python Client

```python
from thermomaven_client import ThermoMavenClient

# Initialize client
client = ThermoMavenClient("your@email.com", "password")
client.app_key = "your_app_key"
client.app_id = "your_app_id"

# Login
result = client.login()
if result["code"] == "0":
    print("Login successful!")
    
    # Get devices
    devices = client.get_my_devices()
    print(f"Found {len(devices)} devices")
    
    # Get user info
    user_info = client.get_user_info()
    print(f"User: {user_info['userName']}")
```

### 🏠 Home Assistant

#### Lovelace Card
```yaml
type: entities
title: 🔥 BBQ Monitor
entities:
  - entity: sensor.thermomaven_grill_probe_1
    name: Steak Temperature
    icon: mdi:food-steak
  - entity: sensor.thermomaven_grill_probe_2
    name: Chicken Temperature
    icon: mdi:food-drumstick
  - entity: sensor.thermomaven_grill_battery
    name: Battery Level
    icon: mdi:battery
```

#### Temperature Graph
```yaml
type: history-graph
title: Temperature History
entities:
  - sensor.thermomaven_grill_probe_1
  - sensor.thermomaven_grill_probe_2
hours_to_show: 3
refresh_interval: 0
```

#### Automation - Steak Ready Alert
```yaml
automation:
  - alias: "🍖 Steak Ready Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.thermomaven_grill_probe_1
      above: 60  # 60°C
    condition:
      - condition: state
        entity_id: input_boolean.bbq_active
        state: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🍖 BBQ Alert"
          message: "Steak is ready! ({{ states('sensor.thermomaven_grill_probe_1') }}°C)"
          data:
            push:
              sound: "US-EN-Alexa-Temperature-Reached.wav"
```

#### Automation - Low Battery Warning
```yaml
automation:
  - alias: "🔋 Low Battery Warning"
    trigger:
      platform: numeric_state
      entity_id: sensor.thermomaven_grill_battery
      below: 20
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Low Battery"
          message: "ThermoMaven battery is low ({{ states('sensor.thermomaven_grill_battery') }}%)"
```

## 🔐 Authentication & Security

The ThermoMaven API uses:
- **MD5 signature** for request authentication
- **Client certificates (P12)** for MQTT connections
- **AWS IoT Core** for secure real-time messaging
- **Automatic certificate management** (download → convert → use → cleanup)

## 🌍 Regional Support

- **🇺🇸 US Region**: `us-west-2` (Oregon) - `a2ubmaqm3a642j-ats.iot.us-west-2.amazonaws.com`
- **🇪🇺 EU Region**: `eu-central-1` (Frankfurt) - `a2ubmaqm3a642j-ats.iot.eu-central-1.amazonaws.com`

**Auto-detection**: The integration automatically detects your region from your account settings.

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/thermomaven-homeassistant.git
cd thermomaven-homeassistant
pip install -r requirements.txt
```

### Testing the Python Client

```bash
cd api
# Test API connection
python thermomaven_client.py

# Test MQTT connection
python thermomaven_mqtt_client.py
```

### Testing in Home Assistant

1. Copy `custom_components/thermomaven` to your HA config folder
2. Restart Home Assistant
3. Add the integration via UI

### Debugging

Enable debug logging in Home Assistant:
```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.thermomaven: debug
    custom_components.thermomaven.thermomaven_api: debug
    paho.mqtt: debug
```

View logs: **Settings** → **System** → **Logs**

## 📋 Requirements

### Home Assistant Integration
- Home Assistant Core 2023.1.0+
- Internet connection (for MQTT)
- Valid ThermoMaven account

**Dependencies** (auto-installed):
- `paho-mqtt>=1.6.1`
- `pyOpenSSL>=23.0.0`
- `cryptography>=41.0.0`

### Python Client (Standalone)
- Python 3.8+
- `requests>=2.31.0`
- `python-dotenv>=1.0.0`
- `paho-mqtt>=1.6.1`
- `pyOpenSSL>=23.0.0`
- `cryptography>=41.0.0`

## 🐛 Troubleshooting

### Common Issues

#### Sensors showing "Unavailable" after restart/reload
**✅ FIXED in v1.3.0!** The integration now:
- Waits for MQTT device list before creating sensors
- Forces coordinator refresh with proper timing
- All sensors update immediately after reload

#### No devices showing in Home Assistant
- ✅ **Check**: Your ThermoMaven devices are paired with your account in the mobile app
- ✅ **Check**: Devices are powered on and connected to WiFi
- ✅ **Check**: Home Assistant logs for MQTT connection success
- ✅ **Solution**: Reload the integration: **Settings** → **Integrations** → **ThermoMaven** → **⋮** → **Reload**

#### MQTT connection fails
- ✅ **Check**: Internet connection
- ✅ **Check**: Firewall allows port 8883 (MQTT SSL)
- ✅ **Check**: ThermoMaven credentials are correct
- ✅ **Check**: Logs for: `✅ MQTT device list received`

#### Diagnostic Information
Check the **Battery** sensor attributes to view:
- `mqtt_device_id`: MQTT identifier (should NOT be null)
- `device_serial`: Physical serial number
- `api_share_id`: API share identifier (if shared device)
- `wifi_rssi`: WiFi signal strength

See **[DIAGNOSTIC_GUIDE.md](MD/DIAGNOSTIC_GUIDE1.3.0.md)** for detailed troubleshooting.

### Getting Help

1. **Enable debug logs**: See [Development](#-development) section
2. **Check diagnostics**: View Battery sensor attributes
3. **GitHub Issues**: [Create an issue](https://github.com/yourusername/thermomaven-homeassistant/issues)
4. **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an **unofficial integration** and is not affiliated with or endorsed by ThermoMaven. This project was created by reverse-engineering the official mobile app for educational and personal use purposes.

**Use at your own risk.** The authors are not responsible for any issues that may arise from using this software.

## 🤝 Contributing

We welcome contributions! Please:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints where possible
- Include tests for new features
- Update documentation as needed

## 🆕 What's New in v1.3.0

### 🏆 Major Improvements
- **✅ RELOAD NOW WORKS!** Complete fix for reload/restart issues
  - Existing sensors properly refresh after reload
  - Forces coordinator refresh with optimal timing
  - All sensors update with latest temperature data
  - **NO MORE "Unavailable" after reload!**

### 📊 Enhanced Sensors
- **17 sensors per device** (up from 5):
  - 5 area temperature zones (Tip → Handle)
  - Ambient & target temperature
  - 3 cooking time sensors (total, current, remaining)
  - Cooking mode & state
  - Probe battery (separate from device battery)
  - WiFi signal strength (RSSI)

### 🌍 Multi-Language Support
- 6 languages fully supported: English, French, Spanish, Portuguese, German, Chinese
- All sensor names and states translated
- Automatic language detection from Home Assistant

### ⚡ Performance
- Smart API caching (API called every 5 minutes instead of 10 seconds = 98% reduction)
- MQTT as primary data source for real-time updates
- Intelligent device merging between API and MQTT data

See **[CHANGELOG.md](CHANGELOG.md)** for complete version history.

## 📞 Support & Community

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/yourusername/thermomaven-client/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/yourusername/thermomaven-client/discussions)
- **🏠 Home Assistant**: [Community Forum](https://community.home-assistant.io/)
- **📖 Documentation**: [Wiki](https://github.com/yourusername/thermomaven-client/wiki)

---

**🔥 Made with ❤️ for the BBQ and cooking community**

*Happy grilling! 🍖🔥*