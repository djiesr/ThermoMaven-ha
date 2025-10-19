# 📁 ThermoMaven Integration Structure

This document describes the file structure and organization of the ThermoMaven Home Assistant integration.

## 📂 Repository Structure

```
thermomaven-homeassistant/
│
├── 📁 custom_components/thermomaven/   # Main integration files
│   ├── __init__.py                      # Integration setup & coordinator
│   ├── config_flow.py                   # Configuration UI flow
│   ├── const.py                         # Constants and defaults
│   ├── manifest.json                    # Integration metadata
│   ├── sensor.py                        # Sensor platform
│   ├── services.yaml                    # Services definition
│   ├── strings.json                     # UI strings (English)
│   ├── thermomaven_api.py               # REST API & MQTT client
│   └── 📁 translations/                 # Multi-language support
│       ├── README.md                    # Translation guide
│       ├── en.json                      # English
│       ├── fr.json                      # French
│       ├── es.json                      # Spanish
│       ├── pt.json                      # Portuguese
│       ├── de.json                      # German
│       └── zh-Hans.json                 # Chinese Simplified
│
├── 📁 api/                              # Standalone Python clients
│   ├── thermomaven_client.py            # REST API client
│   ├── thermomaven_mqtt_client.py       # MQTT client
│   ├── env.example                      # Environment variables template
│   ├── QUICKSTART.md                    # Quick start guide
│   ├── API_ENDPOINTS.md                 # API documentation
│   ├── MQTT_GUIDE.md                    # MQTT guide
│   └── FINDING_APPKEY.md                # How to find API keys
│
├── 📄 README.md                         # Main documentation
├── 📄 ARCHITECTURE.md                   # Technical architecture
├── 📄 CHANGELOG.md                      # Version history
├── 📄 INTEGRATION_STRUCTURE.md          # This file
├── 📄 LICENSE                           # MIT License
├── 📄 VERSION                           # Current version (1.3.0)
└── 📄 requirements.txt                  # Python dependencies
```

## 🔧 Core Integration Files

### `__init__.py` (Main Integration)
**Purpose**: Integration setup and data coordination

**Key Components**:
- `async_setup_entry()`: Entry point for integration setup
- `ThermoMavenDataUpdateCoordinator`: Manages data updates and merging
- Cache system for device persistence
- MQTT synchronization logic

**Responsibilities**:
1. Login to ThermoMaven API
2. Setup MQTT connection
3. Wait for MQTT device list
4. Merge API and MQTT data
5. Create and manage sensors
6. Handle reload/restart scenarios

### `config_flow.py` (Configuration UI)
**Purpose**: User interface for configuration

**Features**:
- Login form (email/password)
- Region selection (auto-detected)
- Validation of credentials
- Error handling and user feedback

**Flow**:
1. User enters credentials
2. Validate via API login
3. Store encrypted credentials
4. Create config entry

### `const.py` (Constants)
**Purpose**: Centralized constants and configuration

**Contains**:
- Domain name
- Platform list
- Default values
- API endpoints
- MQTT broker URLs
- Region mappings

### `sensor.py` (Sensor Platform)
**Purpose**: Sensor entity definitions

**Sensor Types**:
1. **Temperature Sensors** (7):
   - Area 1-5 (Tip → Handle)
   - Ambient
   - Target

2. **Cooking Sensors** (5):
   - Total cook time
   - Current cook time
   - Remaining cook time
   - Cooking mode
   - Cooking state

3. **Battery & Connectivity** (3):
   - Device battery
   - Probe battery
   - WiFi signal (RSSI)

**Features**:
- Translation support
- State classes
- Device classes
- Diagnostic attributes
- Icon handling

### `thermomaven_api.py` (API & MQTT Client)
**Purpose**: Communication with ThermoMaven services

**API Functions**:
- `async_login()`: Authenticate user
- `async_get_my_devices()`: Get owned devices
- `async_get_shared_devices()`: Get shared devices
- `async_sync_user_devices()`: Trigger device sync

**MQTT Functions**:
- `async_setup_mqtt()`: Setup MQTT connection
- `async_wait_for_mqtt_device_list()`: Wait for device list
- `_on_mqtt_message()`: Process MQTT messages
- Certificate management (download, convert, cleanup)

**Message Types**:
- `user:device:list`: Complete device list
- `WT10:status:report`: Temperature updates (and WT02, WT06, WT07, WT09, WT11)

### `manifest.json` (Metadata)
**Purpose**: Integration metadata for Home Assistant

**Contains**:
- Integration name and version
- Documentation URL
- Issue tracker URL
- Dependencies (paho-mqtt, pyOpenSSL, cryptography)
- Configuration flow support
- IoT class (cloud_push)

### `strings.json` (UI Strings)
**Purpose**: User interface text (English)

**Sections**:
- Configuration step titles
- Form field labels
- Error messages
- Abort reasons

### `services.yaml` (Services)
**Purpose**: Service definitions (if any)

Currently: Placeholder for future services like manual sync, calibration, etc.

## 🌍 Translation System

### Translation Files (`translations/*.json`)

**Structure**:
```json
{
  "config": {
    "step": {
      "user": { ... }
    },
    "error": { ... },
    "abort": { ... }
  },
  "entity": {
    "sensor": {
      "area_1_tip": { "name": "..." },
      ...
    }
  },
  "entity_component": {
    "_": {
      "state": {
        "cooking": "...",
        "idle": "...",
        ...
      }
    }
  }
}
```

**Languages Supported**:
- 🇬🇧 English (en) - Default
- 🇫🇷 French (fr)
- 🇪🇸 Spanish (es)
- 🇵🇹 Portuguese (pt)
- 🇩🇪 German (de)
- 🇨🇳 Chinese (zh-Hans)

## 📚 Documentation Files

### User Documentation
- **README.md**: Main user guide
- **HOMEASSISTANT_INSTALLATION.md**: Installation instructions
- **QUICKSTART.md**: Quick start for Python client

### Technical Documentation
- **ARCHITECTURE.md**: System architecture and data flow
- **INTEGRATION_STRUCTURE.md**: This file
- **CHANGELOG.md**: Version history

### Version-Specific Docs (MD/)
- Architecture details for v1.3.0
- Diagnostic guides
- Startup sequence
- Translation info
- Fix explanations

### API Documentation (api/)
- REST API endpoints
- MQTT protocol
- Finding API keys

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────┐
│                  __init__.py                         │
│  ┌───────────────────────────────────────────────┐  │
│  │  ThermoMavenDataUpdateCoordinator             │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │  _async_update_data()                   │  │  │
│  │  │  ├─> Merge API + MQTT data              │  │  │
│  │  │  ├─> Update cache                       │  │  │
│  │  │  └─> Return merged devices              │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────┬───────────────────────────────┘  │
│                  │ coordinator.data                 │
└──────────────────┼──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                  sensor.py                           │
│  ┌───────────────────────────────────────────────┐  │
│  │  ThermoMavenSensor                            │  │
│  │  ├─> native_value (reads from coordinator)   │  │
│  │  ├─> extra_state_attributes                  │  │
│  │  └─> translation_key                         │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│             thermomaven_api.py                       │
│  ┌───────────────────────────────────────────────┐  │
│  │  ThermoMavenAPI                               │  │
│  │  ├─> REST API calls                          │  │
│  │  ├─> MQTT connection                         │  │
│  │  ├─> Certificate management                  │  │
│  │  └─> Message processing                      │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                   │
                   ▼
          ┌────────────────┐
          │ ThermoMaven    │
          │ Cloud API      │
          │ + AWS IoT MQTT │
          └────────────────┘
```

## 🎯 Key Design Decisions

### 1. Coordinator Pattern
- **Why**: Centralized data management
- **Benefit**: Single source of truth, efficient updates
- **Implementation**: `ThermoMavenDataUpdateCoordinator`

### 2. Cache System
- **Why**: Persist device IDs across restarts
- **Benefit**: MQTT updates work after HA restart
- **Implementation**: In-memory cache, dual indexing (name + ID)

### 3. Translation Keys
- **Why**: Support multiple languages
- **Benefit**: Automatic localization based on HA language
- **Implementation**: JSON translation files + translation_key in sensors

### 4. MQTT + API Hybrid
- **Why**: API for setup, MQTT for real-time updates
- **Benefit**: Fast updates + reliable authentication
- **Implementation**: API at startup, MQTT for ongoing updates

### 5. Active MQTT Wait
- **Why**: Ensure device list before sensor creation
- **Benefit**: Sensors always have correct deviceId
- **Implementation**: `async_wait_for_mqtt_device_list()` with timeout

## 🧪 Testing Structure

### Manual Testing
1. First installation
2. Reload integration
3. Restart Home Assistant
4. Multiple devices
5. Shared devices
6. Different languages

### Debugging
Enable debug logging:
```yaml
logger:
  default: info
  logs:
    custom_components.thermomaven: debug
    custom_components.thermomaven.thermomaven_api: debug
```

## 📝 Development Workflow

### Adding a New Sensor
1. Define in `sensor.py`:
   - Add to `SENSOR_TYPES`
   - Set translation_key
   - Define device_class, state_class

2. Add translations in `translations/*.json`:
   ```json
   "entity": {
     "sensor": {
       "new_sensor": {
         "name": "Sensor Name"
       }
     }
   }
   ```

3. Extract data in `sensor.py`:
   - Update `native_value` property
   - Add to `extra_state_attributes` if needed

### Adding a New Language
1. Copy `translations/en.json` to `translations/XX.json`
2. Translate all strings
3. Update README.md with new language

### Modifying API Calls
1. Update `thermomaven_api.py`
2. Test with standalone client in `api/`
3. Update API documentation in `api/API_ENDPOINTS.md`

## 🔒 Security Considerations

### Stored Data
- **Email**: Plain text (config entry)
- **Password**: Encrypted by Home Assistant
- **Certificates**: Temporary, deleted after use
- **Cache**: In-memory only, no sensitive data

### Network Communication
- **API**: HTTPS with MD5 signature
- **MQTT**: TLS with client certificates
- **Regions**: Auto-detected, user can override

## 🚀 Future Enhancements

### Potential Additions
- [ ] Service: Manual device sync
- [ ] Service: Calibrate temperature
- [ ] Binary sensors: Probe connected/disconnected
- [ ] Number entities: Target temperature control
- [ ] Switch entities: Cooking mode selection
- [ ] Diagnostic sensors: Last update time
- [ ] Config options: Update intervals

### Documentation Improvements
- [ ] Developer guide
- [ ] API testing suite
- [ ] Video tutorials
- [ ] FAQ section

---

**Version**: 1.3.0  
**Last Updated**: January 18, 2025  
**Maintainer**: [Your Name]

For questions or contributions, see [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) (if exists).

