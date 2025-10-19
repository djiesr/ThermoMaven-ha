# 🌍 ThermoMaven v1.4.5 - Documentation & Translation Update

**Release Date:** January 19, 2025  
**Type:** Improvement Release  
**Focus:** Documentation & Internationalization

## 🎯 What's New

This release improves **documentation** and **translations** for better international support.

### 📝 README in English

**Complete README translation:**
- ✅ Professional English documentation
- ✅ Better accessibility for international users
- ✅ Clear and concise content
- ✅ Focused on Home Assistant usage

**Improved sections:**
- Installation (HACS + Manual)
- Configuration steps
- Entity list with examples
- Practical usage examples
- Comprehensive troubleshooting

### 🚧 Roadmap Added

**Future features planned for v1.5.0:**

1. **Target Temperature Synchronization**
   - Update `sensor.thermomaven_*_target_temperature` from Climate
   - Bidirectional sync between sensor ↔ climate

2. **Cook Time Control**
   - Set target cooking duration
   - Alarms when time elapsed
   - Remaining time management

3. **Cooking Mode Management**
   - Select cooking mode (Smart, Manual, etc.)
   - Custom cooking presets
   - Temperature profiles by food type

**Future improvements:**
- Temperature history graphs
- Advanced notifications
- Customizable presets
- Multiple timers
- Enhanced multi-zone management

### 🌍 Climate Translation Fix

**Problem:**
- ❌ Climate entity names were always in English
- ❌ Not respecting Home Assistant language setting

**Fixed:**
- ✅ Added `_attr_translation_key` to climate entities
- ✅ Climate names now properly translated
- ✅ Works with all 6 supported languages

**Translation keys:**
```python
probe_1_control → "Probe 1 Control" (EN) / "Contrôle Sonde 1" (FR)
probe_2_control → "Probe 2 Control" (EN) / "Contrôle Sonde 2" (FR)
```

**Supported languages:**
- 🇬🇧 English
- 🇫🇷 French
- 🇪🇸 Spanish
- 🇵🇹 Portuguese
- 🇩🇪 German
- 🇨🇳 Chinese

## 🔄 Upgrade

### Via HACS (Recommended)

1. **HACS** → **Integrations** → **ThermoMaven**
2. Click **Update** to v1.4.5
3. **Restart Home Assistant**

### Manual Update

1. Download [v1.4.5](https://github.com/djiesr/thermomaven-ha/releases/tag/v1.4.5)
2. Extract to `/config/custom_components/thermomaven/`
3. Restart Home Assistant

## ✅ What You'll Get

After updating:

### Climate Entities (Translated)
- Entity names in your Home Assistant language
- Consistent translations across all sensors and climate entities
- Better user experience

### Professional Documentation
- README in English for international users
- Clear roadmap for future development
- Better organized content

## 📊 All Features from v1.4.0+

### 🎛️ Climate Control
- Set target temperature (32-572°F / 0-300°C)
- Start/stop cooking sessions
- HVAC modes: Off, Heat, Auto
- Preset modes: Cooking, Ready, Resting, Remove

### 🌡️ Temperature Monitoring
- Real-time updates via MQTT
- 17+ sensors per device
- Multi-probe support
- Battery and WiFi monitoring

### ⚡ Performance (v1.4.4 fixes)
- Target temperature persists correctly
- API calls reduced by 95%
- MQTT topic detection fixed for all models

## 🐛 Known Issues

None currently reported.

## 📝 Breaking Changes

**None.** Fully backward compatible with v1.4.0+.

## 📚 Documentation

- [README](README.md) - Now in English!
- [Climate Control Guide](CLIMATE_CONTROL_GUIDE.md)
- [Changelog](CHANGELOG.md)
- [Architecture](ARCHITECTURE.md)

## 💬 Feedback

- 🐛 **Bugs**: [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- 🌍 **Translation Help**: Contributions welcome!

## 🔮 What's Next

See the [Roadmap](README.md#-roadmap-to-do) section in README for planned features.

v1.5.0 will focus on:
- Target Temperature synchronization
- Cook Time control
- Cooking Mode management

---

**Full Changelog:** [v1.4.4...v1.4.5](https://github.com/djiesr/thermomaven-ha/compare/v1.4.4...v1.4.5)

---

**Enjoy the improved documentation and translations!** 🌍🎉

