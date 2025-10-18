# ThermoMaven v1.1.4 - Release Summary

## 🌍 Multi-Region Support Release

**Version**: 1.1.4  
**Date**: October 18, 2025  
**Status**: Ready for Release

---

## 🎯 Executive Summary

Version 1.1.4 adds comprehensive multi-region support to the ThermoMaven Home Assistant integration. Users can now select their country during setup, and the integration automatically connects to the appropriate regional API endpoint (European or Global).

---

## ✨ Key Features

### 1. Country Selection
- 30 supported countries
- User-friendly dropdown selector during setup
- Default: United States (US)

### 2. Smart API Routing
- **European API** (`api-de.iot.thermomaven.com`): 25 European countries
- **Global API** (`api.iot.thermomaven.com`): 5 countries (AU, CA, NZ, US, ZA)

### 3. Dynamic Region Headers
- `x-region` header now uses selected country code
- Examples: `FR`, `CA`, `DE`, `US`
- Ensures proper backend regional configuration

### 4. Official Branding
- Uses Home Assistant's official ThermoMaven logos
- Professional appearance in UI

---

## 🌍 Supported Regions

| Region | Countries | API Endpoint |
|--------|-----------|--------------|
| **Europe** | AT, BE, BG, CH, CZ, DE, DK, ES, FI, FR, HU, IE, IS, IT, LU, NL, NO, PL, PT, RO, RS, SE, SK, TR, UK | `api-de.iot.thermomaven.com` |
| **Rest of World** | AU, CA, NZ, US, ZA | `api.iot.thermomaven.com` |

---

## 📊 Changes Overview

### Modified Files (8)
1. `custom_components/thermomaven/const.py` - Country definitions & API URLs
2. `custom_components/thermomaven/config_flow.py` - Region selector
3. `custom_components/thermomaven/thermomaven_api.py` - Dynamic API routing
4. `custom_components/thermomaven/__init__.py` - Region passing
5. `custom_components/thermomaven/strings.json` - Field translations
6. `custom_components/thermomaven/translations/en.json` - English localization
7. `custom_components/thermomaven/translations/fr.json` - French localization
8. `custom_components/thermomaven/manifest.json` - Version bump

### New Files (2)
1. `RELEASE_NOTES_1.1.4.md` - Detailed release notes
2. `SUMMARY_v1.1.4.md` - This file

### Updated Files (2)
1. `CHANGELOG.md` - Added v1.1.4 entry
2. `VERSION` - Updated to 1.1.4

---

## 🔄 Migration Path

### From v1.1.2 to v1.1.4

**Breaking Change**: Configuration structure changed

**Migration Steps**:
1. Remove existing integration
2. Restart Home Assistant (optional but recommended)
3. Re-add integration
4. Select country during setup
5. Enter credentials

**Why**: The configuration schema now includes a required `region` field that wasn't present in v1.1.2.

---

## ✅ Quality Assurance

### Code Quality
- ✅ No linter errors (only expected import warnings)
- ✅ Type safety maintained
- ✅ Backwards compatibility for API (default region: US)

### Documentation
- ✅ CHANGELOG updated
- ✅ Release notes created
- ✅ Translation files updated (EN/FR)
- ✅ Code comments added

### Testing Checklist
- [ ] Test European country selection (e.g., France)
- [ ] Test non-European country selection (e.g., Canada)
- [ ] Verify correct API endpoint is used
- [ ] Verify `x-region` header contains country code
- [ ] Test device discovery with new region settings
- [ ] Test MQTT connection with regional API

---

## 📦 Release Artifacts

### GitHub Release Contents
1. Source code (automatic)
2. `RELEASE_NOTES_1.1.4.md`
3. `CHANGELOG.md` (updated)
4. Tag: `v1.1.4`

### HACS Compatibility
- ✅ `manifest.json` version updated
- ✅ No new dependencies
- ✅ Compatible with existing HACS structure

---

## 📝 Release Notes for Users

**Title**: v1.1.4 - Multi-Region Support 🌍

**Summary**: 
This release adds country/region selection during setup. Choose your country and the integration automatically connects to the correct ThermoMaven API server (European or Global). Supports 30 countries worldwide.

**Upgrade Notice**:
⚠️ You'll need to remove and re-add the integration after updating. Your devices will be rediscovered automatically.

**Note**: Version 1.1.3 was skipped.

---

## 🎯 Success Criteria

- [x] Version bumped to 1.1.4
- [x] All code changes implemented
- [x] Translations updated
- [x] Documentation complete
- [x] No breaking linter errors
- [x] Release notes written
- [ ] GitHub release created
- [ ] HACS release validated

---

## 🚀 Next Steps

1. **Commit Changes**
   ```bash
   git add .
   git commit -m "Release v1.1.4 - Multi-Region Support"
   ```

2. **Create Tag**
   ```bash
   git tag -a v1.1.4 -m "v1.1.4 - Multi-Region Support"
   ```

3. **Push to GitHub**
   ```bash
   git push origin main
   git push origin v1.1.4
   ```

4. **Create GitHub Release**
   - Go to GitHub → Releases → New Release
   - Tag: `v1.1.4`
   - Title: `v1.1.4 - Multi-Region Support 🌍`
   - Description: Copy from `RELEASE_NOTES_1.1.4.md`
   - Attach any additional files if needed

5. **Verify HACS**
   - HACS should automatically detect the new version
   - Users can update via HACS UI

---

## 📚 References

- [CHANGELOG.md](CHANGELOG.md) - Full changelog
- [RELEASE_NOTES_1.1.4.md](RELEASE_NOTES_1.1.4.md) - Detailed release notes
- [REGION_ANALYSIS.md](REGION_ANALYSIS.md) - Regional API analysis
- [GitHub Repository](https://github.com/djiesr/thermomaven-ha)

---

**Release Prepared By**: AI Assistant  
**Review Status**: Ready for Review  
**Release Status**: Ready to Ship 🚢

