# ThermoMaven Home Assistant Integration - Release Notes v1.1.5b1

## 🐛 Bug Fixes

### Critical Fixes
- **Fixed sensor duplication issue**: Resolved problem where multiple sensors were being created for the same device during MQTT updates
- **Fixed MQTT data showing as "unavailable"**: Corrected MQTT temperature updates not being properly processed and displayed
- **Improved device tracking**: Enhanced device persistence to prevent duplicate entity creation

### Technical Improvements
- **Enhanced sensor management**: Implemented persistent device tracking using `coordinator._added_devices` to prevent duplicate sensor creation
- **Better MQTT data handling**: Improved processing of MQTT status reports and temperature updates
- **Data persistence**: Added logic to preserve previous device data when API doesn't return new data but MQTT sends updates

## 🔧 Changes Made

### Files Modified
- `sensor.py`: Fixed sensor duplication by implementing persistent device tracking
- `__init__.py`: Improved MQTT data processing and device data persistence
- `thermomaven_api.py`: Enhanced MQTT message handling for status reports

### Key Improvements
1. **Sensor Duplication Fix**: 
   - Sensors are now only created once per device
   - Persistent tracking prevents duplicate entity creation during coordinator updates
   
2. **MQTT Data Processing**:
   - Temperature updates via MQTT now properly update sensor values
   - Status reports are correctly processed and stored
   - Device data is preserved between API calls
   
3. **Better Error Handling**:
   - Improved logging for debugging MQTT issues
   - Better fallback to previous device data when API is unavailable

## 🚀 What's New

### For Users
- **No more duplicate sensors**: Each device will only show one set of sensors
- **Real-time temperature updates**: MQTT temperature updates now work correctly
- **Better reliability**: Improved handling of network issues and API unavailability

### For Developers
- **Cleaner logs**: Better logging for debugging MQTT and sensor issues
- **Improved architecture**: Better separation of concerns between API and MQTT data
- **Enhanced error handling**: More robust error handling throughout the integration

## 📋 Testing Notes

This is a **beta release** that addresses critical issues reported by users:

### Issues Fixed
- ✅ Sensor duplication during MQTT updates
- ✅ MQTT temperature data showing as "unavailable"
- ✅ Device tracking and persistence issues

### Testing Recommended
- Verify only one set of sensors per device
- Confirm MQTT temperature updates work in real-time
- Test device persistence during network interruptions

## 🔄 Migration Notes

- **No breaking changes**: This release is fully backward compatible
- **No configuration changes required**: Existing configurations will work without modification
- **Automatic cleanup**: Duplicate sensors from previous versions will be automatically cleaned up

## 📝 Known Issues

- None identified in this beta release

## 🎯 Next Steps

- Monitor user feedback for any remaining issues
- Plan for stable release 1.1.5 based on beta feedback
- Continue improving MQTT reliability and performance

---

**Release Date**: October 18, 2025  
**Version**: 1.1.5b1 (Beta)  
**Compatibility**: Home Assistant 2023.1+  
**Status**: Beta Release - Testing Recommended
