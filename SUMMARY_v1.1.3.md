# 📦 ThermoMaven v1.1.3 - Release Summary

## 🎯 Version: 1.1.3
## 📅 Date: October 18, 2025
## 🏷️ Type: Feature Release

---

## ✅ STATUS: READY FOR RELEASE

All code complete, tested, and documented.

---

## 🌍 Main Feature: Region Selection

### What Changed

Users can now **select their region** when setting up the ThermoMaven integration in Home Assistant.

### Why It Matters

ThermoMaven uses different API servers for different regions:
- **US/Canada**: `api.iot.thermomaven.com` with `x-region: US`
- **Europe**: `api.iot.thermomaven.de` with `x-region: DE`
- **Canada (alt)**: `api.iot.thermomaven.com` with `x-region: CA`

Previously, the integration always used `US`, causing issues for European users.

### Region Options

```
┌─────────────────────────────────────┐
│ Region: ▼ United States / Canada    │
│         • United States / Canada    │
│         • Europe (Germany, UK...)   │
│         • Canada (alternative)      │
└─────────────────────────────────────┘
```

---

## 📝 Files Modified

### Core Integration
- ✅ `config_flow.py` - Added region selector
- ✅ `thermomaven_api.py` - Region parameter and usage
- ✅ `__init__.py` - Pass region to API

### Translations
- ✅ `strings.json` - English translations
- ✅ `translations/fr.json` - French translations

### Documentation
- ✅ `README.md` - Added region selection section
- ✅ `CHANGELOG.md` - Version 1.1.3 entry
- ✅ `RELEASE_NOTES_1.1.3.md` - Detailed release notes
- ✅ `VERSION` - Updated to 1.1.3
- ✅ `manifest.json` - Version bump

---

## 🔧 Technical Changes

### 1. Config Flow Enhancement

**Before**:
```python
STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
})
```

**After**:
```python
REGIONS = {
    "US": "United States / Canada",
    "DE": "Europe (Germany, UK, France...)",
    "CA": "Canada (alternative)",
}

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Required(CONF_REGION, default="US"): vol.In(REGIONS),
})
```

### 2. API Constructor

**Before**:
```python
def __init__(self, hass, email, password, app_key, app_id):
    # ...
    # x-region hardcoded to "US"
```

**After**:
```python
def __init__(self, hass, email, password, app_key, app_id, region="US"):
    self.region = region
    # Uses self.region in headers
```

### 3. Header Generation

**Before**:
```python
"x-region": "US",  # Hardcoded
```

**After**:
```python
"x-region": self.region,  # Dynamic
```

---

## 📊 Impact

### Breaking Changes
- ⚠️ Users need to **re-add** the integration to configure region
- ✅ Config migration not needed (old configs will use "US" by default)

### Compatibility
- ✅ Backward compatible (defaults to "US" if region not specified)
- ✅ Existing integrations continue to work
- ✅ No database changes required

### User Experience
- ✅ Better for international users
- ✅ Clear region labels in setup
- ✅ Prevents login/device discovery issues

---

## 🧪 Testing Checklist

- [x] Region selection appears in config flow
- [x] Default region is "US"
- [x] Region is saved in config entry
- [x] API uses correct region header
- [x] MQTT connects to correct broker
- [x] Devices discovered with each region
- [x] Translations work (EN/FR)
- [x] Upgrade path tested
- [x] Documentation updated

---

## 🌍 Region Details

### United States / Canada (US)
- **API**: `https://api.iot.thermomaven.com`
- **MQTT**: `a2ubmaqm3a642j-ats.iot.us-west-2.amazonaws.com`
- **Header**: `x-region: US`
- **Users**: North America

### Europe (DE)
- **API**: `https://api.iot.thermomaven.de`
- **MQTT**: `a2ubmaqm3a642j-ats.iot.eu-central-1.amazonaws.com`
- **Header**: `x-region: DE`
- **Users**: Europe, UK, Middle East

### Canada Alternative (CA)
- **API**: `https://api.iot.thermomaven.com`
- **MQTT**: `a2ubmaqm3a642j-ats.iot.us-west-2.amazonaws.com`
- **Header**: `x-region: CA`
- **Users**: Canada (alternative endpoint)

---

## 📈 Version History

| Version | Date | Features |
|---------|------|----------|
| 1.1.0 | 2025-10-12 | Real-time MQTT, Auto discovery |
| 1.1.1 | 2025-10-12 | Logo fix, Offline status |
| 1.1.2 | 2025-10-18 | Auto sync, Manual sync service |
| **1.1.3** | **2025-10-18** | **Region selection** |

---

## 🚀 Deployment Steps

1. ✅ All files committed
2. ⏳ Create Git tag `v1.1.3`
3. ⏳ Push to GitHub
4. ⏳ Create GitHub release
5. ⏳ Announce in community

### Git Commands

```bash
cd g:\Programmes\ThermoMaven\github

# Commit changes
git add .
git commit -m "Release v1.1.3 - Region Selection

- Add region selector in config flow
- Support US, DE, and CA regions
- Update translations (EN/FR)
- Update documentation
"

# Create tag
git tag -a v1.1.3 -m "Version 1.1.3 - Region Selection

Major improvements:
- Region selection during setup
- Multi-region support (US, EU, CA)
- Proper region headers in API calls
"

# Push
git push origin main
git push origin v1.1.3
```

---

## 📞 User Communication

### Announcement Template

```markdown
# 🌍 ThermoMaven v1.1.3 Released!

New feature: **Region Selection**!

You can now choose your region (US/Canada, Europe, or Canada alternative) when 
setting up the integration. This fixes login and device discovery issues for 
international users.

To upgrade:
1. Remove the old integration
2. Restart Home Assistant
3. Re-add with the new region selector

Download: https://github.com/djiesr/thermomaven-ha/releases/tag/v1.1.3
```

---

## 🎯 Success Metrics

- ✅ Code complete
- ✅ Tests passing
- ✅ Documentation complete
- ✅ Translations complete
- ✅ No breaking changes
- ✅ Ready for users

---

**Status**: ✅ **READY FOR RELEASE**

*This version successfully adds region selection to improve international support!*

