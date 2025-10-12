# Changelog

## [1.1.0] - 2025-10-12 - Real-Time MQTT & Complete Integration 🎉

### 🎊 Major Release - Fully Functional Integration!

This release marks the **first fully functional version** of the ThermoMaven Home Assistant integration with real-time MQTT updates!

### ✨ Major New Features

#### 🚀 Real-Time MQTT Updates (~10 seconds)
- **Device-specific topic subscription**: Automatically subscribes to each device's MQTT topic
- **Instant temperature updates**: Receives temperature changes every ~10 seconds
- **Push-based architecture**: No polling, server pushes updates automatically
- **Zero HTTP overhead**: Temperature updates via MQTT only (no REST API calls)

#### 🎨 Dynamic Entity Creation
- **Automatic device discovery**: Entities created when devices appear via MQTT
- **No restart required**: New devices added on-the-fly
- **Duplicate prevention**: Tracks added devices to avoid duplicates

#### 🌡️ Accurate Temperature Conversion
- **Fixed Fahrenheit to Celsius conversion**: Correctly converts from °F/10 to °C
- **Example**: 748 (raw) → 74.8°F → 23.8°C ✅

#### 💾 Smart Device Caching
- **Persistent device list**: Caches devices between coordinator updates
- **Resilient to API failures**: Uses cached data when REST API returns empty
- **Seamless updates**: Temperature updates work with cached device list

#### 🎨 Visual Improvements
- **Custom icon**: Added icon.png for better visual identity
- **Professional branding**: Integration now has proper logo

### 🔧 Technical Improvements

#### MQTT Enhancements
- Subscribe to user topic: `app/user/{userId}/sub`
- Subscribe to device topics: `app/WT10/{deviceId}/sub`
- Handle `user:device:list` messages for device discovery
- Handle `WT10:status:report` messages for temperature updates
- Reduced REST API polling to 5 minutes (MQTT is primary)

#### Coordinator Optimizations
- Device list persistence across updates
- Smart fallback to cached devices
- Immediate refresh on MQTT messages
- Enhanced logging for debugging

#### Code Quality
- Comprehensive debug logging
- Better error handling
- Type safety improvements
- Documentation updates

### 📊 Performance Metrics

| Metric | Before | After |
|--------|--------|-------|
| **Temperature update latency** | 60-180s | ~10s ⚡ |
| **HTTP requests/hour** | 60 | 12 |
| **Device discovery** | Manual restart | Automatic |
| **Temperature accuracy** | Wrong (°C/10) | Correct (°F→°C) |

### 🐛 Bug Fixes
- ✅ Fixed temperature conversion (was treating °F as °C)
- ✅ Fixed entities not appearing when devices discovered via MQTT
- ✅ Fixed device list disappearing when REST API returns empty
- ✅ Fixed MQTT not subscribing to device-specific topics
- ✅ Fixed coordinator losing device data on status updates

### 📝 Files Modified
- `custom_components/thermomaven/__init__.py`: Device caching & coordinator logic
- `custom_components/thermomaven/sensor.py`: Dynamic entity creation & temperature conversion
- `custom_components/thermomaven/thermomaven_api.py`: Device topic subscription & MQTT handling
- `custom_components/thermomaven/manifest.json`: Version bump to 1.1.0
- `README.md`: Complete rewrite with integration documentation
- Added `icon.png`: Custom integration logo

### 🎯 What's Working Now
- ✅ **Real-time temperature monitoring** (10-second updates)
- ✅ **Automatic device discovery** via MQTT
- ✅ **Battery level tracking**
- ✅ **Multi-probe support** (P1, P2, P4, G1, G2, G4)
- ✅ **Accurate temperature conversion**
- ✅ **Stable entity creation**
- ✅ **Resilient to API failures**

### 🚀 Upgrade Instructions
1. Copy updated `custom_components/thermomaven/` folder
2. Restart Home Assistant
3. Your devices will appear automatically within seconds!

### 🎉 Success!
This version is **production-ready** and fully functional! 🎊

---

## [1.0.3] - 2025-10-11

### Added
- Initial MQTT support
- Certificate handling for AWS IoT Core
- Basic device discovery

### Fixed
- Authentication issues
- Certificate conversion errors

---

## [1.0.2] - 2025-10-10

### Added
- REST API client
- User authentication
- Device listing endpoints

---

## [1.0.1] - 2025-10-09

### Added
- Config flow for Home Assistant
- Basic integration structure

---

## [1.0.0] - 2025-10-08

### Added
- Initial release
- Basic authentication
- Project structure
