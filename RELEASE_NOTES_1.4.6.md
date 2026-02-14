# 🌍 ThermoMaven v1.4.6 - European API Server Fix

**Release Date:** February 14, 2025  
**Type:** Bug Fix Release  
**Focus:** European Region Connectivity

## 🎯 What's Fixed

This release aligns the **European API endpoint** with the official ThermoMaven app, fixing potential connection issues for users outside North America.

### 🔧 API URL Change (Europe)

| Before | After |
|--------|-------|
| `api-de.iot.thermomaven.com` | `api.iot.thermomaven.de` |

**Why this change?**
- The official ThermoMaven mobile app uses `api.iot.thermomaven.de` for European countries
- Our integration was using a different subdomain (`api-de.iot.thermomaven.com`)
- This alignment ensures reliability for European users (France, Germany, UK, etc.)

### 🌍 Affected Regions

**European countries** (25 countries) now use the correct server:
- AT, BE, BG, CH, CZ, DE, DK, ES, FI, FR, HU, IE, IS, IT, LU, NL, NO, PL, PT, RO, RS, SE, SK, TR, UK

**No change** for:
- US, CA, AU, NZ, ZA (still `api.iot.thermomaven.com`)

## 🔄 Upgrade

### Via HACS (Recommended)

1. **HACS** → **Integrations** → **ThermoMaven**
2. Click **Update** to v1.4.6
3. **Restart Home Assistant**

### Manual Update

1. Download [v1.4.6](https://github.com/djiesr/thermomaven-ha/releases/tag/v1.4.6)
2. Extract to `/config/custom_components/thermomaven/`
3. Restart Home Assistant

## ✅ What You'll Get

- ✅ **European users:** Improved connection reliability
- ✅ **Alignment** with ThermoMaven's official app architecture
- ✅ **No breaking changes** for existing configurations

## 📝 Breaking Changes

**None.** Fully backward compatible. European users may need to reconfigure if they had manual workarounds.

## 🙏 Credits

Thanks to the community member who contributed the pull request aligning the API endpoint with the official app documentation!

---

**Full Changelog:** [v1.4.5...v1.4.6](https://github.com/djiesr/thermomaven-ha/compare/v1.4.5...v1.4.6)

---

**Enjoy improved connectivity in Europe!** 🌍✨
