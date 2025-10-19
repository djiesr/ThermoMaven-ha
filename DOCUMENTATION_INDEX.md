# 📚 ThermoMaven Documentation Index

Welcome to the ThermoMaven Home Assistant Integration documentation!

**Current Version**: 1.3.0  
**Last Updated**: January 18, 2025

---

## 🚀 Quick Start

Start here if you're new to ThermoMaven:

1. **[README.md](README.md)** - Main user guide and overview
2. **[Quick Start Guide](api/QUICKSTART.md)** - Get started in 5 minutes
3. **[Installation Guide](#installation)** - Step-by-step installation

---

## 📖 Documentation by Category

### 🏠 Installation & Setup

| Document | Description | For |
|----------|-------------|-----|
| [README.md](README.md) | Complete user guide and overview | Everyone |
| [Home Assistant Installation](MD/HOMEASSISTANT_INSTALLATION.md) | Detailed HA installation steps | New users |
| [Quick Start](api/QUICKSTART.md) | Python client quick start | Developers |
| [Finding App Key](api/FINDING_APPKEY.md) | How to find API credentials | Advanced users |

### 🆕 Version 1.3.0

| Document | Description | For |
|----------|-------------|-----|
| [Release Notes 1.3.0](RELEASE_NOTES_1.3.0.md) | What's new in v1.3.0 | Everyone |
| [Upgrade Guide](UPGRADE_GUIDE.md) | How to upgrade from older versions | Existing users |
| [Changelog](CHANGELOG.md) | Complete version history | Everyone |

### 🏗️ Technical Documentation

| Document | Description | For |
|----------|-------------|-----|
| [Architecture](ARCHITECTURE.md) | System architecture & data flow | Developers |
| [Integration Structure](INTEGRATION_STRUCTURE.md) | File structure & organization | Developers |
| [Startup Sequence](MD/STARTUP_SEQUENCE1.3.0.md) | Detailed startup flow | Developers |
| [API Endpoints](api/API_ENDPOINTS.md) | REST API documentation | Developers |
| [MQTT Guide](api/MQTT_GUIDE.md) | MQTT protocol details | Developers |

### 🔧 Troubleshooting & Support

| Document | Description | For |
|----------|-------------|-----|
| [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md) | Troubleshooting steps | Everyone |
| [Fix: Restart Issue](MD/FIX_RESTART_ISSUE1.3.0.md) | How restart issue was fixed | Technical users |
| [Upgrade Guide](UPGRADE_GUIDE.md) | Troubleshooting upgrades | Existing users |

### 🌍 Internationalization

| Document | Description | For |
|----------|-------------|-----|
| [Translations Guide](MD/TRANSLATIONS1.3.0.md) | Multi-language support info | Everyone |
| [Translation Files](custom_components/thermomaven/translations/README.md) | How to add translations | Translators |

### 📝 Miscellaneous

| Document | Description | For |
|----------|-------------|-----|
| [LICENSE](LICENSE) | MIT License | Everyone |
| [VERSION](VERSION) | Current version number | Developers |
| [Requirements](requirements.txt) | Python dependencies | Developers |

---

## 📂 Documentation Structure

```
github/
├── 📄 README.md                         ⭐ Start here!
├── 📄 DOCUMENTATION_INDEX.md            📚 This file
│
├── 📁 Version 1.3.0 Docs
│   ├── RELEASE_NOTES_1.3.0.md          🎉 What's new
│   ├── UPGRADE_GUIDE.md                 ⬆️ Upgrade instructions
│   ├── CHANGELOG.md                     📋 Version history
│   ├── ARCHITECTURE.md                  🏗️ Technical architecture
│   └── INTEGRATION_STRUCTURE.md         📁 File structure
│
├── 📁 MD/ - Detailed v1.3.0 Docs
│   ├── ARCHITECTURE1.3.0.md            🏗️ Architecture details
│   ├── CHANGELOG1.3.0.md               📋 Detailed changelog
│   ├── DIAGNOSTIC_GUIDE1.3.0.md        🔧 Troubleshooting
│   ├── FIX_RESTART_ISSUE1.3.0.md       ✅ Restart fix details
│   ├── HOMEASSISTANT_INSTALLATION.md   🏠 HA installation
│   ├── README1.3.0.md                  📖 Version-specific readme
│   ├── STARTUP_SEQUENCE1.3.0.md        🚀 Startup flow
│   └── TRANSLATIONS1.3.0.md            🌍 Translation info
│
├── 📁 api/ - Python Client & API Docs
│   ├── thermomaven_client.py           🐍 REST API client
│   ├── thermomaven_mqtt_client.py      📡 MQTT client
│   ├── API_ENDPOINTS.md                📚 API documentation
│   ├── MQTT_GUIDE.md                   📡 MQTT guide
│   ├── QUICKSTART.md                   ⚡ Quick start
│   └── FINDING_APPKEY.md               🔑 Finding API keys
│
└── 📁 custom_components/thermomaven/
    ├── __init__.py                      🔧 Integration core
    ├── sensor.py                        📊 Sensor platform
    ├── thermomaven_api.py               🌐 API & MQTT client
    ├── manifest.json                    📋 Metadata
    └── translations/                    🌍 6 languages
        ├── en.json, fr.json, es.json
        ├── pt.json, de.json, zh-Hans.json
        └── README.md                    📖 Translation guide
```

---

## 🎯 Documentation by User Type

### 👤 End Users (Home Assistant Users)

**Essential Reading**:
1. [README.md](README.md) - Overview and features
2. [Home Assistant Installation](MD/HOMEASSISTANT_INSTALLATION.md) - How to install
3. [Release Notes 1.3.0](RELEASE_NOTES_1.3.0.md) - What's new
4. [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md) - When things go wrong

**Optional Reading**:
- [Upgrade Guide](UPGRADE_GUIDE.md) - If upgrading from older version
- [Translations](MD/TRANSLATIONS1.3.0.md) - Multi-language info

### 🔧 Advanced Users

**Essential Reading**:
1. [README.md](README.md) - Overview
2. [Architecture](ARCHITECTURE.md) - How it works
3. [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md) - Troubleshooting
4. [API Endpoints](api/API_ENDPOINTS.md) - API details

**Optional Reading**:
- [MQTT Guide](api/MQTT_GUIDE.md) - MQTT protocol
- [Finding App Key](api/FINDING_APPKEY.md) - API credentials
- [Startup Sequence](MD/STARTUP_SEQUENCE1.3.0.md) - Detailed flow

### 💻 Developers & Contributors

**Essential Reading**:
1. [Integration Structure](INTEGRATION_STRUCTURE.md) - File organization
2. [Architecture](ARCHITECTURE.md) - System design
3. [Startup Sequence](MD/STARTUP_SEQUENCE1.3.0.md) - Initialization
4. [API Endpoints](api/API_ENDPOINTS.md) - REST API
5. [MQTT Guide](api/MQTT_GUIDE.md) - MQTT protocol

**For Development**:
- [Translation Guide](custom_components/thermomaven/translations/README.md) - Add languages
- [Fix: Restart Issue](MD/FIX_RESTART_ISSUE1.3.0.md) - Problem-solving approach
- Source code in `custom_components/thermomaven/`

### 🌍 Translators

**Essential Reading**:
1. [Translations Guide](MD/TRANSLATIONS1.3.0.md) - Overview
2. [Translation Files](custom_components/thermomaven/translations/README.md) - How to contribute
3. [Integration Structure](INTEGRATION_STRUCTURE.md) - File locations

---

## 🔍 Find Information By Topic

### Installation
- [Home Assistant Installation](MD/HOMEASSISTANT_INSTALLATION.md)
- [Quick Start](api/QUICKSTART.md)
- [Requirements](requirements.txt)

### Features
- [README.md](README.md) - Complete feature list
- [Release Notes 1.3.0](RELEASE_NOTES_1.3.0.md) - New features
- [Changelog](CHANGELOG.md) - Feature history

### Troubleshooting
- [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md) - Main troubleshooting
- [Upgrade Guide](UPGRADE_GUIDE.md) - Upgrade issues
- [Fix: Restart Issue](MD/FIX_RESTART_ISSUE1.3.0.md) - Technical fix details

### API & MQTT
- [API Endpoints](api/API_ENDPOINTS.md) - REST API
- [MQTT Guide](api/MQTT_GUIDE.md) - MQTT protocol
- [Finding App Key](api/FINDING_APPKEY.md) - Credentials

### Architecture
- [Architecture](ARCHITECTURE.md) - Overall design
- [Integration Structure](INTEGRATION_STRUCTURE.md) - File structure
- [Startup Sequence](MD/STARTUP_SEQUENCE1.3.0.md) - Boot process

### Languages
- [Translations Guide](MD/TRANSLATIONS1.3.0.md) - Info
- [Translation Files](custom_components/thermomaven/translations/README.md) - How to
- 6 supported languages: en, fr, es, pt, de, zh-Hans

---

## 📊 Sensors Documentation

### 17 Sensors per Device

**Temperature Sensors (7)**:
- Area 1 (Tip) - Most precise zone
- Area 2, 3, 4 - Middle zones
- Area 5 (Handle) - Coolest zone
- Ambient Temperature
- Target Temperature

**Cooking Sensors (5)**:
- Total Cook Time
- Current Cook Time
- Remaining Cook Time
- Cooking Mode
- Cooking State

**Battery & Connectivity (3)**:
- Device Battery
- Probe Battery
- WiFi Signal (RSSI)

See [README.md - Sensors](README.md#what-youll-get) for details.

---

## 🆘 Need Help?

### Quick Links

- **🐛 Found a bug?** → [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- **💡 Feature request?** → [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- **❓ Question?** → [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md)
- **📖 Documentation unclear?** → [Open an issue](https://github.com/djiesr/thermomaven-ha/issues)

### Debug Logging

Enable for troubleshooting:
```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.thermomaven: debug
    custom_components.thermomaven.thermomaven_api: debug
```

---

## 🎯 Common Use Cases

### "I want to install ThermoMaven"
1. Read: [README.md](README.md)
2. Follow: [Home Assistant Installation](MD/HOMEASSISTANT_INSTALLATION.md)
3. Verify: [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md)

### "I want to upgrade to v1.3.0"
1. Read: [Release Notes 1.3.0](RELEASE_NOTES_1.3.0.md)
2. Follow: [Upgrade Guide](UPGRADE_GUIDE.md)
3. Troubleshoot: [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md)

### "I want to understand how it works"
1. Read: [Architecture](ARCHITECTURE.md)
2. Read: [Integration Structure](INTEGRATION_STRUCTURE.md)
3. Read: [Startup Sequence](MD/STARTUP_SEQUENCE1.3.0.md)

### "I want to use the Python client"
1. Read: [Quick Start](api/QUICKSTART.md)
2. Read: [API Endpoints](api/API_ENDPOINTS.md)
3. Read: [MQTT Guide](api/MQTT_GUIDE.md)

### "Something is not working"
1. Check: [Diagnostic Guide](MD/DIAGNOSTIC_GUIDE1.3.0.md)
2. Check: [Upgrade Guide - Troubleshooting](UPGRADE_GUIDE.md#-troubleshooting)
3. Report: [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)

### "I want to add a translation"
1. Read: [Translations Guide](MD/TRANSLATIONS1.3.0.md)
2. Follow: [Translation Files](custom_components/thermomaven/translations/README.md)
3. Submit: Pull Request on GitHub

---

## 📅 Version History

- **v1.3.0** (Jan 2025) - Reload fix, 17 sensors, multi-language
- **v1.2.x** (Jan 2025) - Bug fixes and improvements
- **v1.2.0** (Jan 2025) - Expanded sensors, translations
- **v1.1.x** (2024) - Initial releases

See [CHANGELOG.md](CHANGELOG.md) for complete history.

---

## 🙏 Credits

**Maintainer**: @djiesr  
**Contributors**: Community testers and translators  
**Technologies**: Home Assistant, AWS IoT Core, ThermoMaven API

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

**Last Updated**: January 18, 2025  
**Version**: 1.3.0  
**Status**: Current Release

---

**Happy Grilling! 🍖🔥**

