# 🐛 ThermoMaven v1.4.4 - Target Temperature Fix

**Release Date:** January 19, 2025  
**Type:** Bug Fix Release  
**Focus:** Climate Control Temperature Persistence

## 🎯 What's Fixed

This release fixes a critical bug where the **target temperature was not persisting** after being set in the climate entity.

### 🐛 Problem

When users set a target temperature in the climate control:
- ❌ Temperature would appear to change
- ❌ But immediately revert to the previous value
- ❌ User input was being overwritten by coordinator refresh
- ❌ Device hadn't confirmed the change yet

### ✅ Solution

Implemented a **local temperature cache** with smart synchronization:

**How it works now:**
1. 🎯 **Instant Update** - Temperature displays immediately when you set it
2. 📡 **MQTT Command** - Command sent to device in background
3. ⏱️ **Smart Wait** - 2-second delay for device to process
4. ✅ **Confirmation** - Device confirms via MQTT status report
5. 🔄 **Sync** - Cache cleared when device confirms (±0.5°F tolerance)

**Result:**
- ✅ Temperature persists correctly
- ✅ No more flickering or reverting
- ✅ Smooth user experience
- ✅ Reliable MQTT communication

## 🔧 Technical Details

### Changes Made

**File: `custom_components/thermomaven/climate.py`**

- Added `_target_temperature_override` attribute for local caching
- Modified `target_temperature` property to check cache first
- Updated `async_set_temperature` to:
  - Store temperature locally immediately
  - Call `async_write_ha_state()` for instant UI update
  - Send MQTT command in background
  - Wait 2 seconds before refresh
- Smart cache clearing when device confirms (±0.5°F tolerance)

### Before (Bug):
```
User sets 165°F → MQTT sent → Coordinator refreshes → ❌ Reverts to old value
```

### After (Fixed):
```
User sets 165°F → ✅ Shows 165°F instantly → MQTT sent → Wait 2s → Device confirms → ✅ Stays at 165°F
```

## 🔄 Upgrade Instructions

### Via HACS (Recommended)

1. Open **HACS** → **Integrations**
2. Find **ThermoMaven**
3. Click **⋮** → **Update** (or Redownload)
4. Select version **1.4.4**
5. **Restart Home Assistant**

### Manual Update

1. Download [v1.4.4 from GitHub](https://github.com/djiesr/thermomaven-ha/releases/tag/v1.4.4)
2. Replace `custom_components/thermomaven/climate.py`
3. Restart Home Assistant

## ✅ Verification

After updating, test the fix:

1. Open a climate entity: `climate.thermomaven_[device]_probe_1_control`
2. Set a new target temperature (e.g., 165°F)
3. ✅ Temperature should **stay at 165°F** (not revert)
4. After ~2 seconds, device confirms the change
5. Everything works smoothly!

## 📊 What's Included from Previous Versions

All features from v1.4.0+ are included:

### 🎛️ Climate Control
- Climate entities for each probe
- Set target temperature (32-572°F / 0-300°C)
- Start/stop cooking sessions
- HVAC modes: Off, Heat, Auto
- Preset modes: Cooking, Ready, Resting, Remove

### 🌡️ Temperature Monitoring
- Real-time updates via MQTT
- 17+ sensors per device
- Multi-probe support (up to 4)
- Battery and WiFi monitoring

## 🐛 Known Issues

None currently reported.

If you find any issues, please report them on [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues).

## 📝 Breaking Changes

**None.** This release is fully backward compatible with v1.4.0+.

## 💬 Feedback

This fix was implemented based on user feedback. Thank you for reporting the issue!

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- 💡 **Suggestions:** [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- 📖 **Documentation:** [README](README.md) | [Climate Guide](CLIMATE_CONTROL_GUIDE.md)

## 🔮 What's Next

Future improvements (v1.5.0+):
- 📊 Cooking history graphs
- ⏰ Timer and alarm controls
- 🎨 Custom cooking presets
- 📱 Enhanced notifications

---

**Full Changelog:** https://github.com/djiesr/thermomaven-ha/blob/main/CHANGELOG.md

---

**Enjoy your fixed climate control!** 🎉🌡️

