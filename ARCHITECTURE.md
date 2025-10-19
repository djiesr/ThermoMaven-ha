# 🏗️ ThermoMaven Integration Architecture

## 📊 Data Flow Overview

### 1️⃣ Initial Startup

```
┌─────────────────┐
│  Home Assistant │
│    Startup      │
└────────┬────────┘
         │
         ├──> 📡 ThermoMaven API
         │    ├─> My Devices (deviceId: valid)
         │    └─> Shared Devices (deviceId: None ❌)
         │
         └──> 🔌 MQTT Connection
              └─> user:device:list
                  └─> deviceId: 216510650012434433 ✅
```

### 2️⃣ Data Merging (FIRST TIME)

```
┌──────────────┐      ┌──────────────┐
│  API Data    │      │  MQTT Data   │
├──────────────┤      ├──────────────┤
│ deviceName: X│      │ deviceName: X│
│ deviceId: ❌ │  +   │ deviceId: ✅ │
│ shareId: ✅  │      │ deviceSn: ✅ │
└──────┬───────┘      └──────┬───────┘
       │                     │
       └──────────┬──────────┘
                  │ MERGE
                  ▼
         ┌────────────────┐
         │ Merged Device  │
         ├────────────────┤
         │ deviceName: X  │
         │ deviceId: ✅   │
         │ deviceSn: ✅   │
         │ shareId: ✅    │
         └────────┬───────┘
                  │
                  ▼
         💾 Persistent Cache
            - cache[name] = device
            - cache[deviceId] = device
```

### 3️⃣ Home Assistant Restart

```
┌─────────────────┐
│  HA Restart     │
└────────┬────────┘
         │
         ├──> 📡 API (deviceId: None ❌)
         │
         ├──> 🔌 MQTT Setup
         │    └─> Wait for device list (max 10s)
         │
         ▼
    ✅ MQTT device list received
         │
         ▼
    🔄 Merge API + MQTT data
         │
         ▼
    💾 Cache updated
         │
         ▼
    📋 Devices with valid deviceId
         │
         ▼
    🔌 MQTT updates work! ✅
```

## 🔄 Cache System

### Cache Structure

```python
{
  # By device name
  "ThermoMaven G1 - 2ESA": {
    "deviceId": "216510650012434433",
    "deviceSn": "WTA0CC30A14A6B2ESA",
    "deviceName": "ThermoMaven G1 - 2ESA",
    "deviceShareId": 243747941034328064,
    ...
  },
  
  # By device ID (for MQTT updates)
  "216510650012434433": {
    ... (same data)
  }
}
```

### Benefits

1. **🚀 Persistence between restarts**
   - Merged data is kept in memory
   - Automatic restoration on startup

2. **🔄 Dual indexing**
   - By name: to match with API
   - By ID: to match with MQTT

3. **💾 Lightweight and fast**
   - In-memory only
   - No external files
   - Automatic rebuild via MQTT

## 📡 MQTT Management

### MQTT Messages Processed

#### 1. `user:device:list` (Complete list)
```json
{
  "cmdType": "user:device:list",
  "cmdData": {
    "devices": [{
      "deviceId": "216510650012434433",
      "deviceName": "ThermoMaven G1 - 2ESA",
      "deviceSn": "WTA0CC30A14A6B2ESA",
      "lastStatusCmd": { ... }
    }]
  }
}
```
**Action**: Merge with API + Cache update

#### 2. `WT10:status:report` (Temperature update)
```json
{
  "cmdType": "WT10:status:report",
  "deviceId": "216510650012434433",
  "cmdData": {
    "globalStatus": "online",
    "batteryValue": 68,
    "probes": [{ "curTemperature": 797 }]
  }
}
```
**Action**: Find device by ID → Update coordinator data

## 🚀 Startup Sequence (v1.3.0)

### Optimized Order

```
1. Login API ✅
   │
2. Create Coordinator
   │
3. Setup MQTT (BEFORE first refresh)
   │
4. ⏳ Wait for MQTT device list (max 10s)
   │
5. ✅ Device list received
   │
6. First data refresh (with MQTT data)
   │
7. Create sensors (with correct deviceId)
   │
8. ✅ Integration ready!
```

### Timeline

```
T=0.0s  : Login API
T=0.5s  : Create Coordinator
T=0.6s  : Setup MQTT start
T=1.0s  : MQTT connected
T=1.2s  : MQTT subscribed to user topic
T=1.3s  : API device sync triggered
T=1.8s  : MQTT receives user:device:list ✅
T=1.8s  : Wait loop exits
T=2.0s  : First refresh with MQTT data
T=2.5s  : Sensors created with correct deviceId
T=3.0s  : Integration ready ✅
```

## 🎯 Scenarios

### ✅ Scenario 1: First Add
1. Config flow → Login API
2. API returns devices (with deviceId: None for shared)
3. MQTT connects → Receives device list
4. **Merge** → Cache created
5. Entities created with correct deviceId ✅

### ✅ Scenario 2: HA Restart
1. HA starts → Load integration
2. API returns devices (deviceId: None)
3. MQTT connects → Waits for device list
4. **Merge with MQTT data** → Cache updated ✅
5. MQTT reconnects → Updates work ✅

### ✅ Scenario 3: Temperature Update
1. MQTT receives `status:report`
2. deviceId extracted from message
3. Search in current devices
4. If not found → **Search in cache** ✅
5. Update applied → Sensors updated ✅

## 🔍 Logs to Monitor

### ✅ Good Operation
```
💾 Cached X device mappings
✅ Restored deviceId from cache for: ThermoMaven G1 - 2ESA (ID: 216510650012434433)
💾 Found device in cache by ID: 216510650012434433
✅ MQTT device list received in 2.3s
✅ Fusion complete: 1 merged devices
```

### ⚠️ Potential Issues
```
⚠️ No cache found for device: ThermoMaven G1 - 2ESA
❌ Device ID 216510650012434433 not found in device list
⚠️ Timeout waiting for MQTT device list after 10s
```

## 🛠️ Maintenance

### When is cache rebuilt?
- On each MQTT `user:device:list` message
- On each API + MQTT merge
- On each temporary device creation

### Does cache persist after restart?
- **Yes** while HA is running
- **No** after complete HA restart
- But it's **automatically rebuilt** on first MQTT connection

### How to clear cache?
The cache rebuilds automatically. To force:
1. Reload the integration
2. Or restart Home Assistant
3. MQTT will rebuild cache automatically

## 📈 Performance

- **Memory**: ~2-5 KB per device (negligible)
- **CPU**: O(1) lookup via dictionary
- **Network**: No impact (data already received)

## 🔐 Security

- Cache in RAM only
- No sensitive data stored
- Automatic rebuild from trusted sources (API + MQTT)

## 📊 Sensor Architecture

Each device creates **17 sensors**:

### Temperature Sensors (7)
- 5 area temperatures (Tip → Handle)
- Ambient temperature
- Target temperature

### Cooking Sensors (5)
- Total cook time
- Current cook time
- Remaining cook time
- Cooking mode
- Cooking state

### Battery & Connectivity (3)
- Device battery
- Probe battery
- WiFi signal (RSSI)

### Translation System
All sensor names and states are translated into 6 languages:
- English (en)
- French (fr)
- Spanish (es)
- Portuguese (pt)
- German (de)
- Chinese Simplified (zh-Hans)

## 🔄 Update Flow

```
[MQTT Update Received]
         │
         ▼
[Extract deviceId from message]
         │
         ▼
[Search in coordinator.data]
         │
    ┌────┴────┐
    │         │
 Found      Not Found
    │         │
    │         ▼
    │   [Search in cache]
    │         │
    └────┬────┘
         │
         ▼
[Update device data]
         │
         ▼
[Notify all sensors]
         │
         ▼
[Sensors display new values] ✅
```

## 📝 Files Structure

```
custom_components/thermomaven/
├── __init__.py              # Integration setup & coordinator
├── config_flow.py           # Configuration UI
├── const.py                 # Constants
├── manifest.json            # Integration metadata
├── sensor.py                # Sensor entities
├── services.yaml            # Services definition
├── strings.json             # UI strings
├── thermomaven_api.py       # API & MQTT client
└── translations/            # Multi-language support
    ├── en.json
    ├── fr.json
    ├── es.json
    ├── pt.json
    ├── de.json
    └── zh-Hans.json
```

## 🎯 Key Classes

### `ThermoMavenAPI`
- Handles REST API authentication
- Manages MQTT connection
- Processes incoming MQTT messages
- Maintains device list

### `ThermoMavenDataUpdateCoordinator`
- Merges API and MQTT data
- Manages cache
- Updates sensors
- Handles refresh intervals

### `ThermoMavenSensor`
- Displays sensor data
- Handles translations
- Updates from coordinator

## 🔧 Configuration

The integration stores:
- Email (username)
- Password (encrypted)
- Region (auto-detected)

MQTT certificates are:
- Downloaded dynamically
- Converted P12 → PEM
- Cleaned up after use
- Never stored permanently

---

**For more details, see:**
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [README.md](README.md) - User guide
- [DIAGNOSTIC_GUIDE.md](MD/DIAGNOSTIC_GUIDE1.3.0.md) - Troubleshooting

