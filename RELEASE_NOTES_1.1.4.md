# 🌍 ThermoMaven v1.1.4 - Multi-Region Support

**Release Date**: October 18, 2025

## 🎉 What's New

### Country/Region Selection

This release adds **multi-region support** to the ThermoMaven integration! You can now select your country during setup, and the integration will automatically connect to the correct regional API.

## ✨ New Features

### 🌍 30 Supported Countries

The integration now supports 30 countries across Europe and the rest of the world:

**European Countries** (connected to `api-de.iot.thermomaven.com`):
- Austria (AT), Belgium (BE), Bulgaria (BG), Switzerland (CH)
- Czech Republic (CZ), Germany (DE), Denmark (DK), Spain (ES)
- Finland (FI), France (FR), Hungary (HU), Ireland (IE)
- Iceland (IS), Italy (IT), Luxembourg (LU), Netherlands (NL)
- Norway (NO), Poland (PL), Portugal (PT), Romania (RO)
- Serbia (RS), Sweden (SE), Slovakia (SK), Turkey (TR)
- United Kingdom (UK)

**Rest of World** (connected to `api.iot.thermomaven.com`):
- Australia (AU), Canada (CA), New Zealand (NZ)
- United States (US), South Africa (ZA)

### 🚀 Automatic API Routing

The integration automatically determines which API endpoint to use based on your selected country:
- **European countries** → European API server (Germany)
- **Other countries** → Global API server

### 🔧 Dynamic Region Header

The `x-region` header now dynamically uses your country code (e.g., `FR`, `CA`, `DE`, `US`), ensuring proper regional configuration with ThermoMaven's backend.

### 🎨 Official Home Assistant Logos

The integration now uses the official ThermoMaven logos provided by Home Assistant's brands repository for a more polished look.

## 🔧 Technical Details

### What Changed

1. **Configuration Flow**: Added a country/region dropdown selector during setup
2. **API Client**: Automatically selects the correct API endpoint based on region
3. **Regional Headers**: Uses the selected country code in API requests
4. **Translations**: Full support for English and French translations

### Files Modified

- `const.py`: Added country definitions and API endpoints
- `config_flow.py`: Added region selector
- `thermomaven_api.py`: Dynamic API URL selection and region handling
- `__init__.py`: Region parameter passing
- `strings.json`: Translation keys for region field
- `translations/en.json` & `translations/fr.json`: Localized country selector
- `manifest.json`: Version bump to 1.1.4

## 📦 Installation & Upgrade

### New Installation

1. Download and install the integration via HACS or manually
2. Add the integration from Home Assistant → Settings → Devices & Services
3. **Select your country** from the dropdown
4. Enter your ThermoMaven credentials
5. Your devices will appear automatically!

### Upgrading from v1.1.2

**Important**: Due to the configuration changes, you'll need to re-add the integration:

1. Remove the existing ThermoMaven integration
2. Restart Home Assistant (recommended)
3. Re-add the integration
4. **Select your country** during setup
5. Enter your credentials

The integration will automatically use the correct API endpoint for your region.

## 🐛 Bug Fixes

All features from v1.1.2 are preserved:
- ✅ Automatic device discovery
- ✅ Real-time MQTT updates
- ✅ Manual sync service
- ✅ Multi-probe support

## 📝 Notes

- **Version 1.1.3 was skipped** due to an internal error
- Default region is set to "US" if not specified
- All existing features remain functional

## 🙏 Acknowledgments

Thanks to the Home Assistant community and ThermoMaven users for feedback and testing!

## 📚 Documentation

- [Installation Guide](HOMEASSISTANT_INSTALLATION.md)
- [Changelog](CHANGELOG.md)
- [Region Analysis](REGION_ANALYSIS.md)
- [GitHub Repository](https://github.com/djiesr/thermomaven-ha)

## 💬 Support

If you encounter any issues:
1. Check the [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
2. Enable debug logging in Home Assistant
3. Open a new issue with your logs

---

**Enjoy your ThermoMaven integration with proper regional support!** 🎊

