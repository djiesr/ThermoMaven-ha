# 🔧 ThermoMaven v1.4.1 - HACS Fix Release

**Release Date:** January 19, 2025  
**Type:** Stable Release  
**Focus:** HACS Compatibility & Documentation

## 🎯 What's New

This is a **maintenance release** focused on fixing HACS compatibility and improving documentation.

### 🔧 Fixes & Improvements

#### HACS Compatibility ✅
- **Fixed `.hacs.json` configuration**
  - Removed deprecated `default_branch: release` setting
  - Now correctly uses `main` branch
  - Better version detection in HACS
  - Fixed version format (removed `-beta` suffix)

#### Documentation 📚
- **Simplified README** - Focused on Home Assistant users
  - Clear installation steps (HACS + Manual)
  - Detailed configuration guide with screenshots
  - Complete list of entities created
  - Practical Lovelace card examples
  - Working automation examples
  - Comprehensive troubleshooting section
  
- **Removed technical details** from main README
  - Python client docs moved to separate files
  - Focus on what users see in Home Assistant
  - Better user experience for non-developers

### 🎛️ All v1.4.0 Features Included

This release includes all features from v1.4.0:
- ✅ Climate entities for temperature control
- ✅ Set target temperature (32-572°F / 0-300°C)
- ✅ Start/stop cooking sessions
- ✅ HVAC modes: Off, Heat, Auto
- ✅ Preset modes: Cooking, Ready, Resting, Remove
- ✅ Real-time MQTT commands

## 🔄 Upgrade Instructions

### Via HACS (Recommended)

1. Open **HACS** → **Integrations**
2. Find **ThermoMaven**
3. Click **⋮** → **Redownload** (or **Update** if available)
4. Select version **1.4.1**
5. Click **Download**
6. **Restart Home Assistant**

### Manual Update

1. Download [v1.4.1 from GitHub](https://github.com/djiesr/thermomaven-ha/releases/tag/v1.4.1)
2. Extract and replace files in `/config/custom_components/thermomaven/`
3. Restart Home Assistant

## 📊 Changes from v1.4.0

| Component | Change | Impact |
|-----------|--------|--------|
| `.hacs.json` | Removed `default_branch` | HACS can now find the integration |
| `VERSION` | Updated to 1.4.1 | Version tracking |
| `manifest.json` | Updated version | Integration metadata |
| `README.md` | Simplified | Better user experience |
| `CHANGELOG.md` | Updated | Version history |

## ✅ What You'll Get

After updating to v1.4.1, you'll have:

### 🌡️ Temperature Monitoring
- Real-time temperature updates via MQTT
- 5 area temperature zones per probe
- Ambient and target temperature
- Up to 4 probes depending on model

### 🎛️ Climate Control (v1.4.0+)
- Climate entity for each probe
- Set target temperature
- Start/stop cooking
- Multiple control modes

### ⏱️ Cooking Tracking
- Total, current, and remaining cook time
- Cooking mode and state
- Automatic time calculations

### 🔋 Device Monitoring
- Battery levels (device + probes)
- WiFi signal strength
- Connection status

## 🐛 Known Issues

None currently reported.

If you find any issues, please report them on [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues).

## 📝 Breaking Changes

**None.** This release is fully backward compatible with v1.4.0.

All existing entities and configurations continue to work as before.

## 🎯 Verification

After updating, verify the version:

1. Go to **HACS** → **Integrations** → **ThermoMaven**
2. Version should show **1.4.1**

Or check in the integration:
1. **Settings** → **Devices & Services** → **ThermoMaven**
2. Click on the integration
3. Version info should display 1.4.1

## 💬 Feedback & Support

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- 💡 **Feature Requests:** [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- 📖 **Documentation:** [README](README.md) | [Climate Guide](CLIMATE_CONTROL_GUIDE.md)

## 🙏 Thank You

Thank you for using the ThermoMaven integration! Your feedback helps make it better.

Special thanks to everyone who reported HACS compatibility issues.

## 🔮 What's Next

Future plans (v1.5.0+):
- 📊 Cooking history and graphs
- ⏰ Timer and alarm controls
- 📱 Enhanced notifications
- 🎨 Custom preset modes

---

**Enjoy your updated integration!** 🎉🌡️

