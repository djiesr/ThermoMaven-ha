# 🧪 ThermoMaven v1.4.1-beta - Beta Release Notes

**Release Date:** January 19, 2025  
**Type:** Beta Release  
**Status:** Testing HACS Compatibility

## 📋 What's in This Beta

This is a **maintenance release** focused on improving HACS compatibility and user documentation.

### 🔧 Fixes & Improvements

#### HACS Compatibility
- ✅ Fixed `.hacs.json` configuration to use `main` branch
- ✅ Removed deprecated `default_branch: release` setting
- ✅ Better version detection in HACS

#### Documentation
- 📚 **Simplified README** - Focused on Home Assistant users
  - Clear installation steps (HACS + Manual)
  - Detailed configuration process
  - Complete entity list with examples
  - Practical Lovelace cards and automations
  - Troubleshooting guide
  
- 📖 Removed technical Python client details (kept in separate docs)
- 🎯 Better focus on what users see in Home Assistant

### 🎛️ Features (from v1.4.0)

All features from v1.4.0 are included:
- Climate entities for temperature control
- Set target temperature (32-572°F / 0-300°C)
- Start/stop cooking sessions
- HVAC modes: Off, Heat, Auto
- Preset modes: Cooking, Ready, Resting, Remove
- Real-time MQTT commands

## 🔄 Upgrade from v1.4.0

### Via HACS (Recommended)

1. Open **HACS** → **Integrations**
2. Find **ThermoMaven**
3. Click **⋮** → **Redownload**
4. Wait for v1.4.1-beta to appear
5. Click **Download**
6. **Restart Home Assistant**

### Manual Update

1. Download this release from GitHub
2. Replace files in `/config/custom_components/thermomaven/`
3. Restart Home Assistant

## ✅ What to Test

Please help test this beta by verifying:

### Installation
- [ ] HACS can find and download the integration
- [ ] Manual installation works correctly
- [ ] Version 1.4.1-beta appears in HACS

### Functionality
- [ ] All sensors appear after installation
- [ ] Climate entities are created
- [ ] Temperature control works
- [ ] Real-time MQTT updates function
- [ ] No errors in logs

### Documentation
- [ ] README is clear and helpful
- [ ] Configuration steps are easy to follow
- [ ] Examples work as expected

## 🐛 Known Issues

None reported yet for this beta.

If you find any issues, please report them on [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues).

## 📝 Changes from v1.4.0

| File | Change | Reason |
|------|--------|--------|
| `.hacs.json` | Removed `default_branch` | HACS compatibility |
| `README.md` | Simplified content | Better user experience |
| `VERSION` | Updated to 1.4.1-beta | Version tracking |
| `manifest.json` | Updated version | Integration metadata |

## 🔙 Rollback

If you experience issues, you can rollback to v1.4.0:

**Via HACS:**
1. HACS → ThermoMaven → **⋮** → **Redownload**
2. Select version **1.4.0**
3. Restart Home Assistant

**Manual:**
1. Download [v1.4.0 release](https://github.com/djiesr/thermomaven-ha/releases/tag/v1.4.0)
2. Replace files
3. Restart

## 📊 Testing Period

This beta will be active for approximately **1-2 weeks** (until ~February 2, 2025).

If no major issues are found, it will be promoted to stable v1.4.1.

## 💬 Feedback

Please share your feedback:
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- 💡 **Suggestions:** [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- ✅ **Success Stories:** Comment on this release

## 🙏 Thank You

Thank you for helping test this beta release! Your feedback is invaluable for improving the integration.

---

**⚠️ Beta Warning**

This is a beta release. While it should work correctly, please:
- Test in a non-production environment first if possible
- Report any issues you encounter
- Be prepared to rollback if needed

---

## What's Next?

After this beta stabilizes:
- v1.4.1 (stable) - Documentation and HACS improvements
- v1.5.0 (future) - Additional features (cooking history, alarms, etc.)

---

**Happy Testing!** 🧪🔥

