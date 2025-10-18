# 🌍 ThermoMaven v1.1.3 - Region Selection

## Release Date: October 18, 2025

---

## 🎯 What's New

### Region Selection During Setup

Users can now **select their region** when adding the ThermoMaven integration to Home Assistant!

#### Available Regions:
- 🇺🇸 **United States / Canada** (default)
- 🇪🇺 **Europe** (Germany, UK, France, etc.)
- 🇨🇦 **Canada** (alternative endpoint)

### Why This Matters

ThermoMaven uses **region-specific servers** for API calls and MQTT connections. Previously, the integration always used the US region, which could cause:
- ❌ Login failures for European accounts
- ❌ Empty device lists
- ❌ MQTT connection issues

Now, the integration **automatically uses the correct region** based on your selection! ✅

---

## ✨ New Features

### 1. Region Selection in Config Flow

When adding the integration, you'll see a new **Region** dropdown:

```
┌─────────────────────────────────────┐
│  ThermoMaven Setup                  │
├─────────────────────────────────────┤
│  Email: your@email.com              │
│  Password: ********                 │
│  Region: ▼ United States / Canada   │ ← NEW!
│          • United States / Canada   │
│          • Europe (Germany, UK...)  │
│          • Canada (alternative)     │
└─────────────────────────────────────┘
```

### 2. Proper Region Headers

The integration now sends the correct `x-region` header in all API calls:
- **US/Canada**: `x-region: US`
- **Europe**: `x-region: DE`
- **Canada Alt**: `x-region: CA`

### 3. Region-Specific MQTT Brokers

Automatically connects to the right MQTT broker:
- **US**: `a2ubmaqm3a642j-ats.iot.us-west-2.amazonaws.com`
- **Europe**: `a2ubmaqm3a642j-ats.iot.eu-central-1.amazonaws.com`

---

## 🔧 Technical Details

### Files Modified

- **`config_flow.py`**: Added region selection dropdown with 3 options
- **`thermomaven_api.py`**: Added `region` parameter, uses `self.region` in headers
- **`__init__.py`**: Passes region from config to API client
- **`strings.json`**: Added English translations for region selection
- **`translations/fr.json`**: Added French translations

### API Changes

```python
# Before
api = ThermoMavenAPI(hass, email, password, app_key, app_id)

# After
api = ThermoMavenAPI(hass, email, password, app_key, app_id, region="US")
```

### Config Entry Structure

```json
{
  "email": "user@example.com",
  "password": "********",
  "app_key": "bcd4596f1bb8419a92669c8017bf25e8",
  "app_id": "ap4060eff28137181bd",
  "region": "US"  // NEW!
}
```

---

## 📦 Installation / Upgrade

### New Installation

1. Copy `custom_components/thermomaven` to your HA config folder
2. Restart Home Assistant
3. Go to **Settings** → **Devices & Services** → **Add Integration**
4. Search for **ThermoMaven**
5. **Select your region** ← New step!
6. Enter credentials
7. Done!

### Upgrading from 1.1.2 or earlier

⚠️ **Important**: You'll need to **re-add** the integration to configure your region.

1. **Remove** the existing ThermoMaven integration
2. **Restart** Home Assistant
3. **Re-add** the integration with the new region selector
4. Your devices will reappear automatically

**Note**: Your historical data will be preserved if you keep the same entity IDs.

---

## 🎯 Which Region Should I Choose?

### 🇺🇸 United States / Canada
Choose this if:
- Your account was created in the US or Canada
- Your ThermoMaven app shows temperatures in Fahrenheit by default
- You're located in North America

### 🇪🇺 Europe (Germany, UK, France...)
Choose this if:
- Your account was created in Europe
- Your ThermoMaven app shows temperatures in Celsius by default
- You're located in Europe, UK, or Middle East

### 🇨🇦 Canada (alternative)
Choose this if:
- You're in Canada and the US region doesn't work
- You were instructed to use this region by ThermoMaven support

**Tip**: If you're not sure, start with **United States / Canada** (default).

---

## 🐛 Bug Fixes

This release also includes all fixes from **v1.1.2**:
- ✅ Automatic device discovery (no mobile app required)
- ✅ MQTT synchronization triggers
- ✅ Fallback sync mechanism
- ✅ Manual sync service

And from **v1.1.1**:
- ✅ Logo display fix
- ✅ Better offline status handling
- ✅ Extra state attributes

---

## 🔍 Troubleshooting

### Devices not showing up after upgrade?

1. **Check your region**: Make sure you selected the correct region
2. **Try different regions**: If one doesn't work, try another
3. **Check logs**: Enable debug logging:
   ```yaml
   logger:
     logs:
       custom_components.thermomaven: debug
   ```
4. **Use manual sync**: Developer Tools → Services → `thermomaven.sync_devices`

### How do I know which region I'm on?

Check your ThermoMaven mobile app:
- Open the app
- Go to **Settings** → **About**
- Look for server information

Or check the API URL when logging in (visible in debug logs).

---

## 📊 Version Comparison

| Feature | v1.1.0 | v1.1.1 | v1.1.2 | v1.1.3 |
|---------|--------|--------|--------|--------|
| MQTT Real-time | ✅ | ✅ | ✅ | ✅ |
| Auto device discovery | ✅ | ✅ | ✅ | ✅ |
| Logo display | ❌ | ✅ | ✅ | ✅ |
| Offline status | ❌ | ✅ | ✅ | ✅ |
| Auto sync trigger | ❌ | ❌ | ✅ | ✅ |
| Manual sync service | ❌ | ❌ | ✅ | ✅ |
| **Region selection** | ❌ | ❌ | ❌ | ✅ |

---

## 🎉 Credits

Special thanks to:
- Users who reported region-specific issues
- The Home Assistant community
- ThermoMaven for creating great hardware

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/djiesr/thermomaven-ha/issues)
- **Discussions**: [GitHub Discussions](https://github.com/djiesr/thermomaven-ha/discussions)
- **Documentation**: See [README.md](README.md)

---

## 🔮 What's Next?

Future plans for v1.2.0:
- Historical temperature graphs
- Cooking presets integration
- Advanced automation triggers
- Push notifications

---

**Happy grilling! 🔥🍖**

*Made with ❤️ for the BBQ and cooking community*

