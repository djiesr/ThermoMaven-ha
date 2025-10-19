# Changelog

All notable changes to this project will be documented in this file.

## [1.4.4] - 2025-01-19 🐛

### 🐛 Bug Fix - Target Temperature Persistence

#### Climate Control Fix
- **Fixed target temperature not persisting**
  - Temperature was reverting immediately after being set
  - Coordinator refresh was overwriting user input before device confirmation
  
- **Solution implemented:**
  - Added local temperature cache (`_target_temperature_override`)
  - Temperature updates instantly in UI
  - MQTT command sent in background
  - Wait 2 seconds for device response before refresh
  - Cache cleared when device confirms (±0.5°F tolerance)
  
- **User experience:**
  - ✅ Instant feedback when setting temperature
  - ✅ Temperature persists correctly
  - ✅ Smooth interaction without flickering
  - ✅ Reliable MQTT command delivery

## [1.4.1] - 2025-01-19 🔧

### 🔧 HACS & Documentation Improvements

#### HACS Compatibility
- **Fixed `.hacs.json` configuration**
  - Removed deprecated `default_branch: release`
  - Now uses `main` branch correctly
  - Better version detection in HACS
  - Fixed version format for HACS compatibility

#### Documentation
- **Simplified README**
  - Focused on Home Assistant users
  - Clear installation steps (HACS + Manual)
  - Detailed configuration process
  - Complete entity list and examples
  - Practical Lovelace cards and automations
  - Troubleshooting guide for common issues
  
- Removed technical Python client details
- Better focus on Home Assistant usage

#### All v1.4.0 Features Included
- Climate control entities
- Temperature control via MQTT
- Start/stop cooking sessions
- HVAC and Preset modes

## [1.4.0] - 2025-01-19 🎉

### 🎛️ NEW FEATURE - Climate Control

#### ✨ Climate Entities Added!
- **Full temperature control via MQTT**
  - Set target temperature for each probe
  - Start/stop cooking sessions
  - View current and target temperatures in one entity
  - Preset modes for cooking states

#### 🌡️ Climate Features
- **Climate entity for each probe**:
  - `climate.thermomaven_[device]_probe_1_control`
  - `climate.thermomaven_[device]_probe_2_control`
  - Additional probes for 4-probe models
  
- **Control capabilities**:
  - Set target temperature (32°F - 572°F / 0°C - 300°C)
  - Turn on/off (start/stop cooking)
  - HVAC modes: Off, Heat, Auto
  - Preset modes: Cooking, Ready, Resting, Remove
  
- **Real-time MQTT commands**:
  - Commands published via MQTT to device
  - Automatic topic detection from device list
  - Fallback to standard topic format
  
#### 🔧 Technical Implementation
- **New API methods**:
  - `async_set_probe_temperature()` - Modify target temperature
  - `async_start_cooking()` - Start cooking with target temp
  - `async_stop_cooking()` - Stop/pause cooking
  - `_get_device_pub_topic()` - Auto-detect publish topics

- **MQTT command structure**:
  - Command type: `WT:probe:control`
  - Cooking actions: 1=start, 2=stop, 3=modify
  - Temperature in tenths of degrees F (e.g., 650 = 65.0°F)
  - Probe color detection (bright/dark)

#### 🌍 Translations
- Added climate entity translations in 6 languages
- Consistent naming with sensor entities

## [1.3.0] - 2025-01-18 🎉

### 🏆 MAJOR UPDATE - Reload/Restart Fix

#### ✅ RELOAD NOW WORKS!
- **Complete fix for reload/restart issues**
  - Existing sensors properly refresh after reload
  - Forces coordinator refresh with 0.5s delay for entity registration
  - All sensors update with latest temperature data
  - **NO MORE "Unavailable" after reload!** ✅

#### 🔧 Technical Improvements
- **Optimized startup sequence**:
  1. Login API
  2. Create Coordinator
  3. Setup MQTT (BEFORE first refresh)
  4. Wait actively for MQTT device list (max 10s)
  5. First data refresh with complete data
  6. Create sensors with correct deviceId
  
- **MQTT synchronization enhanced**:
  - Active waiting mechanism for MQTT device list
  - Flag system to track when device list is received
  - Timeout protection (10s) if MQTT is slow
  - Prevents sensor creation with incomplete data

- **Coordinator refresh timing optimized**:
  - Entities fully registered before refresh triggered
  - Proper async handling for entity updates
  - Forces listener update after reload

#### 📊 Complete Sensor Suite
- **17 sensors per thermometer** working perfectly:
  - 5 area temperature sensors (Tip → Handle)
  - Ambient & target temperature
  - 3 cooking time sensors (total, current, remaining)
  - Cooking mode & state
  - Device battery & probe battery
  - WiFi signal strength (RSSI)

- **Real-time MQTT updates** fully functional
- **Temperature, battery, cooking time** - all working!

#### 🌍 Multi-Language Support
- **6 languages fully supported**:
  - 🇬🇧 English (en) - default
  - 🇫🇷 French (fr) - complete translation
  - 🇪🇸 Spanish (es) - complete translation
  - 🇵🇹 Portuguese (pt) - complete translation
  - 🇩🇪 German (de) - complete translation
  - 🇨🇳 Chinese Simplified (zh-Hans) - complete translation

- **Translation system** for all sensor names and states
- **Automatic language detection** from Home Assistant

#### ⚡ Performance Improvements
- **Smart API caching**: API called only every 5 minutes instead of every 10 seconds (98% reduction)
- **MQTT as primary data source** for real-time updates
- **Intelligent device merging** between API and MQTT data
- **Persistent cache system** for device mappings

#### 🔧 Bug Fixes
- Fixed sensor duplication issue during integration reloads
- Fixed MQTT updates not applying to sensors after restart
- Fixed "unavailable" sensor states after reload
- Fixed device ID mismatch between API and MQTT
- Improved device name matching for shared devices
- Fixed MQTT timeout issues on slow connections
- Fixed duplicate entity errors on reload

#### 📚 Documentation
- Added `ARCHITECTURE.md` with technical architecture
- Added `DIAGNOSTIC_GUIDE.md` with troubleshooting steps
- Added `STARTUP_SEQUENCE.md` with detailed startup flow
- Added `TRANSLATIONS.md` with translation guide
- Updated `README.md` with new features
- Comprehensive changelog with version history

---

## [1.2.9] - 2025-01-18

### 🔧 Fixed
- **Critical: Existing sensors not updating after reload**
  - Force coordinator listeners update
  - After reload, existing sensors weren't being notified of new data
  - Added `coordinator.async_update_listeners()` to force entity refresh
  - Existing sensors now update immediately after reload
  - Fixes "Unavailable" state on reload ✅

### 🔍 Enhanced Logging
- Added sensor setup diagnostics
- Shows when entities already exist vs newly created
- Device IDs in coordinator now logged for troubleshooting

---

## [1.2.8] - 2025-01-18

### 🔧 Fixed
- **Critical: MQTT reload timeout**
  - Fixed integration reload not receiving device list
  - Detects if MQTT is already running (reload case)
  - Forces fresh `user:device:list` request on reload
  - Prevents 10-second timeout waiting for device list
  - Sensors now work immediately after reload ✅

### 📊 Result
- ✅ First add: Works perfectly with temperature display
- ✅ Reload: Now gets fresh device list, no timeout
- ✅ Sensors functional in both scenarios

---

## [1.2.7] - 2025-01-18

### 🔧 Fixed
- **Critical: Syntax errors**: Fixed indentation errors
  - Fixed `SyntaxError` in `__init__.py` line 136
  - Fixed `IndentationError` in `thermomaven_api.py` line 141
  
### 🧹 Improved
- **Logs cleaned up**: Reduced verbosity significantly
  - API JSON responses moved to DEBUG level
  - Compact temperature updates: `✅ Temperature updated: Device = 82.2°F (27.9°C)`
  - Final result shows `lastStatusCmd` presence: `[True]` or `[False]`
  - Sensors warn only when data is missing

### 📊 Enhanced
- Serial number format: `WTA0CC30A14A6B2ESA | MQTT: 216510650012434433`

---

## [1.2.6] - 2025-01-18

### 🔧 Fixed
- **DeviceInfo parameter error**: Removed invalid `serial_mqtt` parameter
  - Fixed `TypeError: unexpected keyword argument 'serial_mqtt'`
  - Serial number now shows: `SN | MQTT: device_id` format
  - Both identifiers visible in single field

---

## [1.2.5] - 2025-01-18

### 🔧 Fixed
- **Critical: Sensor values not populating**
  - Force coordinator refresh after sensor creation
  - Sensors now immediately show values instead of "Unavailable"
  - `native_value` is called right after entity registration
  - Temperature data properly loaded on first display

### 🔍 Improved  
- **Diagnostic information enhanced**
  - Serial number now shows both physical SN and MQTT ID
  - Format: `WTA0CC30A14A6B2ESA (MQTT ID: 216510650012434433)`
  - Easier troubleshooting with both identifiers visible
  - API Share ID visible in attributes

### 📝 Result
- ✅ Sensors show temperature immediately after creation
- ✅ No more "Unavailable" state on initial load
- ✅ Diagnostic info clearly visible in device page

---

## [1.2.4] - 2025-01-18

### 🔧 Fixed
- **Critical: MQTT device list validation**
  - Fixed integration reload/restart issues
  - MQTT flag now resets properly on each setup
  - Wait function validates that `user:device:list` is received (not just `status:report`)
  - Device deduplication prevents duplicate entities
  - Fixes "unique ID already exists" errors on reload

### 🐛 Bug Fixes
- Fixed duplicate device entries in coordinator data
- Fixed MQTT wait returning immediately with stale data
- Proper cmdType validation in wait loop

### 🎯 Result
- ✅ Clean reload without duplicate entities
- ✅ Sensors created only once with correct deviceId
- ✅ MQTT updates work immediately after reload

---

## [1.2.3] - 2025-01-18

### ✨ Added
- **Device diagnostic information**
  - Serial number now visible in device page
  - Configuration URL added (links to ThermoMaven app)
  - Suggested area (Kitchen) for new devices

### 🔍 Improved
- **Battery sensor diagnostics**
  - Now shows detailed diagnostic info in attributes:
    - `mqtt_device_id`: MQTT identifier used for real-time updates
    - `api_share_id`: API share identifier if device is shared
    - `device_serial`: Physical serial number
    - `from_user`: User who shared the device
    - `share_status`: Sharing status
  - Centralized `DeviceInfo` creation for consistency
  - Better device information display in Home Assistant UI

### 📚 Documentation
- Added `DIAGNOSTIC_GUIDE.md` with troubleshooting steps
- Detailed explanation of all diagnostic attributes
- Common problems and solutions

---

## [1.2.2] - 2025-01-18

### 🔧 Fixed
- **MQTT synchronization at startup**
  - Integration now waits for MQTT device list before creating sensors
  - Added active waiting mechanism for MQTT device list (max 10 seconds)
  - MQTT setup moved before first data refresh
  - Flag system to track when MQTT device list is received
  - Prevents sensor creation with incomplete data
  - Ensures sensors are always created with correct `deviceId`

### 🚀 Improved
- Startup sequence optimized: MQTT → Wait → Refresh → Create sensors
- Better logging for MQTT readiness state
- Timeout protection (10s) if MQTT is slow to respond

---

## [1.2.1] - 2025-01-18

### 🔧 Fixed
- **Device persistence after restart**
  - Added intelligent caching system to preserve merged device data
  - Devices now maintain their `deviceId` mapping after Home Assistant restart
  - MQTT updates continue to work correctly after reboot
  - Cache stores device mappings by both name and ID for reliability
  - Automatic restoration of `deviceId` for shared devices on startup

### 🚀 Improved
- Better logging for cache operations
- More resilient device matching after restarts

---

## [1.2.0] - 2025-01-18

### ✨ Added
- **17 sensors per device** (up from 2):
  - 🌡️ **5 Area Temperature sensors** (Tip, Area 2-4, Handle)
  - 🌡️ **Ambient Temperature sensor**
  - 🌡️ **Target Temperature sensor**
  - ⏱️ **3 Cooking Time sensors** (Total, Current, Remaining)
  - 🔋 **Probe Battery sensor** (separate from device battery)
  - 📡 **Cooking Mode sensor** (smart, manual, etc.)
  - 📡 **Cooking State sensor** (cooking, charged, charging, idle, standby)
  - 📶 **WiFi Signal sensor** (RSSI in dBm)

- **🌍 Multi-language support**:
  - English (en) - default
  - French (fr) - complete translation
  - Spanish (es) - complete translation
  - Portuguese (pt) - complete translation
  - German (de) - complete translation
  - Chinese Simplified (zh-Hans) - complete translation
  - Translation system for all sensor names and states

- **⚡ Performance improvements**:
  - Smart API caching (API called only every 5 minutes instead of every 10 seconds)
  - MQTT as primary data source for real-time updates
  - Intelligent device merging between API and MQTT data

### 🔧 Fixed
- Fixed sensor duplication issue during integration reloads
- Fixed MQTT updates not applying to sensors
- Fixed "unavailable" sensor states
- Fixed device ID mismatch between API and MQTT
- Improved device name matching for shared devices

### 🏗️ Changed
- Area temperature labels improved: "Area 1 Tip" and "Area 5 Handle"
- Cooking State now uses Home Assistant translation system
- Better logging for debugging API and MQTT data flow
- Entity registry used for persistent device tracking

### 📚 Documentation
- Added `TRANSLATIONS.md` with translation guide
- Updated `README.md` with new features
- Added comprehensive changelog

---

## [1.1.5] - Previous Version

### Features
- Basic temperature and battery monitoring
- MQTT support
- Multi-region support (US, EU, Canada)

---

## Version History Summary

- **1.3.0**: 🎉 Major update - Reload fix + complete sensor suite + multi-language
- **1.2.x**: Bug fixes for reload/restart issues and MQTT synchronization
- **1.2.0**: Major update with 15+ new sensors and translations
- **1.1.5**: Bug fixes and region improvements
- **1.1.3-1.1.4**: Region handling improvements
- **1.1.2**: Working MQTT support (US only)
- **1.1.0-1.1.1**: Initial releases

---

## Upgrade Notes

### Upgrading to 1.3.0
- **No breaking changes**
- New sensors will appear automatically
- Translation will apply based on your Home Assistant language
- If sensors show "Unavailable" after upgrade, simply **reload the integration**

### Configuration Changes
- No configuration changes required
- Existing devices will continue to work
- New sensors are added automatically

