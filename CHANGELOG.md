# Changelog

## [1.1.3] - 2025-10-18 - Region Selection

### ✨ New Features
- **Region selection during setup**: Users can now choose their region (US/Canada, Europe, Canada alternative)
- **Proper region handling**: The integration now sends the correct `x-region` header based on user selection
- **Multi-region support**: Full support for US, DE (Europe), and CA regions

### 🔧 Improvements
- **Better region detection**: Region is saved in config and used for all API calls
- **Region-specific MQTT brokers**: Automatically selects the correct MQTT broker based on region
- **Updated translations**: Added region selection in English and French translations

### 📝 Files Modified
- `custom_components/thermomaven/config_flow.py`: Added region selection dropdown
- `custom_components/thermomaven/thermomaven_api.py`: Added region parameter and usage
- `custom_components/thermomaven/__init__.py`: Pass region to API
- `custom_components/thermomaven/strings.json`: Added region translations
- `custom_components/thermomaven/translations/fr.json`: Added French translations

### 🎯 Region Options
- **US**: United States / Canada (default)
- **DE**: Europe (Germany, UK, France, etc.)
- **CA**: Canada (alternative endpoint)

---

## [1.1.2] - 2025-10-18 - Automatic Device Discovery Fix

### 🐛 Bug Fixes
- **Fixed device discovery requiring mobile app**: Devices are now discovered automatically without needing to open the mobile app
- **Automatic MQTT synchronization**: Integration now triggers device list sync via API after connecting to MQTT
- **Fallback sync mechanism**: If no devices are found, automatic retry (max 3 attempts)

### ✨ Improvements
- **Proactive device sync**: Calls `/app/device/share/my/device/list` and `/app/device/share/shared/device/list` endpoints automatically
- **Multiple sync points**: 
  - On MQTT connection
  - After MQTT setup (with 2s delay for connection stability)
  - Every coordinator update if no devices found (max 3 attempts)
- **Anti-spam protection**: Limited to 3 automatic sync attempts to prevent API overload
- **Manual sync service**: New `thermomaven.sync_devices` service to force sync on-demand
- **Better reliability**: No longer depends on external mobile app to trigger MQTT messages

### 🔍 Root Cause
The ThermoMaven system uses a hybrid REST API + MQTT architecture where:
- MQTT provides real-time updates (temperatures, status)
- REST API calls trigger server-side actions that publish MQTT messages

The `user:device:list` MQTT message is only published when a client calls the device listing endpoints. The mobile app calls these automatically on startup, but the Home Assistant integration was only listening passively.

### 📝 Files Modified
- `custom_components/thermomaven/thermomaven_api.py`: Added `_trigger_device_sync()`, modified `_on_mqtt_connect()` and `async_setup_mqtt()`
- `custom_components/thermomaven/__init__.py`: Added fallback sync with attempt counter, registered `sync_devices` service
- `custom_components/thermomaven/strings.json`: Added service translations
- Added `custom_components/thermomaven/services.yaml`: Service definition
- Added `DEVICE_DISCOVERY_FIX.md`: Detailed technical documentation

### 🎯 Testing
To test the fix:
1. Remove the existing ThermoMaven integration
2. Restart Home Assistant
3. Re-add the integration **without opening the mobile app**
4. Devices should appear within 10-15 seconds automatically

### 🔧 Manual Sync Service
If devices aren't detected automatically:
1. Go to Developer Tools → Services
2. Search for "ThermoMaven: Synchroniser les appareils"
3. Click "Call Service"

Or use in automations:
```yaml
service: thermomaven.sync_devices
```

---

## [1.1.1] - 2025-10-12 - Icon & Status Display Fix

### 🐛 Bug Fixes
- **Fixed logo not appearing**: Added `logo.png` and `issue_tracker` in manifest
- **Fixed "Unavailable" status**: Entities now show empty state instead of "Unavailable" when device is offline
- **Better offline handling**: Devices remain "available" in HA even when powered off

### ✨ Improvements
- **Added extra state attributes**: Each sensor now shows detailed status information
  - Temperature sensors: status, connection, cooking_state, probe_battery
  - Battery sensors: status, battery_status, connection, wifi_rssi
- **Status translations**: "En ligne" / "Hors ligne" / "Inconnu"
- **Better UX**: Users can see device status even when offline

### 📝 Files Modified
- `custom_components/thermomaven/manifest.json`: Added issue_tracker, version 1.1.1
- `custom_components/thermomaven/sensor.py`: Fixed available property, added extra_state_attributes
- `custom_components/thermomaven/strings.json`: Added entity state translations
- Added `custom_components/thermomaven/logo.png`

---

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
