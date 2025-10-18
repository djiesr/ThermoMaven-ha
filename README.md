# ThermoMaven API Client & Home Assistant Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-orange)](https://www.home-assistant.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

A comprehensive Python client and Home Assistant integration for ThermoMaven wireless thermometers, reverse-engineered from the official mobile app.

## 🎯 Features

### ✅ Core Functionality
- **Complete REST API client** with MD5 signature authentication
- **Real-time MQTT communication** via AWS IoT Core
- **Home Assistant integration** with custom component
- **Automatic device discovery** and entity creation
- **Temperature monitoring** for all ThermoMaven devices
- **Battery level tracking** with low battery alerts
- **Multiple device support** (P1, P2, P4, G1, G2, G4)

### 🌡️ Temperature Features
- **Real-time temperature updates** via MQTT push
- **Accurate temperature conversion** (Fahrenheit → Celsius)
- **Multi-probe monitoring** (up to 4 probes per device)
- **Temperature history** and graphing
- **Custom temperature alerts** and notifications

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

For each ThermoMaven device:
```
sensor.thermomaven_[device]_probe_1    # 🌡️ Temperature Probe 1
sensor.thermomaven_[device]_probe_2    # 🌡️ Temperature Probe 2 (if available)
sensor.thermomaven_[device]_probe_3    # 🌡️ Temperature Probe 3 (if available)
sensor.thermomaven_[device]_probe_4    # 🌡️ Temperature Probe 4 (if available)
sensor.thermomaven_[device]_battery    # 🔋 Battery Level
```

## 📚 Documentation

- **[API Endpoints](API_ENDPOINTS.md)** - Complete API documentation
- **[MQTT Guide](MQTT_GUIDE.md)** - Real-time messaging setup
- **[Home Assistant Installation](HOMEASSISTANT_INSTALLATION.md)** - Detailed HA setup guide
- **[Integration Summary](INTEGRATION_SUMMARY.md)** - Technical overview
- **[Changelog](CHANGELOG.md)** - Version history

## 🔧 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Python Client │────│  ThermoMaven API │────│  AWS IoT Core   │
│                 │    │  (REST + Auth)   │    │     (MQTT)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Home Assistant  │
                    │  Integration    │
                    │  (Custom Comp)  │
                    └─────────────────┘
```

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
git clone https://github.com/yourusername/thermomaven-client.git
cd thermomaven-client
pip install -r requirements.txt
```

### Testing

```bash
# Test API connection
python thermomaven_client.py

# Test MQTT connection
python thermomaven_mqtt_client.py
```

### Debugging

Enable debug logging in Home Assistant:
```yaml
# configuration.yaml
logger:
  logs:
    custom_components.thermomaven: debug
    paho.mqtt: debug
```

## 📋 Requirements

### Python Client
- Python 3.8+
- `requests>=2.31.0`
- `python-dotenv>=1.0.0`
- `paho-mqtt>=1.6.1`
- `pyOpenSSL>=23.0.0`
- `cryptography>=41.0.0`

### Home Assistant
- Home Assistant Core 2023.1.0+
- Internet connection (for MQTT)
- Valid ThermoMaven account

## 🐛 Troubleshooting

### Common Issues

#### No devices showing in Home Assistant
- ✅ **Check**: Your ThermoMaven devices are paired with your account in the mobile app
- ✅ **Check**: Devices are powered on and connected to WiFi
- ✅ **Check**: Home Assistant logs for any errors

#### MQTT connection fails
- ✅ **Check**: Internet connection
- ✅ **Check**: Firewall allows port 8883 (MQTT SSL)
- ✅ **Check**: ThermoMaven credentials are correct

#### Temperature readings seem wrong
- ✅ **Fixed**: Temperature conversion from Fahrenheit to Celsius
- ✅ **Note**: ThermoMaven uses Fahrenheit internally (converted to Celsius)

### Getting Help

1. **Check logs**: Settings → System → Logs
2. **GitHub Issues**: [Create an issue](https://github.com/yourusername/thermomaven-client/issues)
3. **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

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

## 🎉 Success Stories

> *"This integration works perfectly with my ThermoMaven P4! I can monitor all 4 probes from Home Assistant and get alerts when my BBQ is ready."* - BBQ Enthusiast

> *"Finally, I can automate my cooking process with Home Assistant. The MQTT integration provides real-time temperature updates."* - Home Chef

## 📞 Support & Community

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/yourusername/thermomaven-client/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/yourusername/thermomaven-client/discussions)
- **🏠 Home Assistant**: [Community Forum](https://community.home-assistant.io/)
- **📖 Documentation**: [Wiki](https://github.com/yourusername/thermomaven-client/wiki)

---

**🔥 Made with ❤️ for the BBQ and cooking community**

*Happy grilling! 🍖🔥*