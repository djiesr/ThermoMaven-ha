# Finding the App Key - SUCCESS! ✅

## Status: FOUND!

**Date**: January 2025  
**Method**: Dynamic analysis using Frida

The `app_key` has been successfully found and the client is now fully functional for authentication!

## Found Values

### US Region
- **App ID**: `ap4060eff28137181bd`
- **App Key**: `bcd4596f1bb8419a92669c8017bf25e8`
- **Base URL**: `https://api.iot.thermomaven.com`

### EU Region (DE)
- **App ID**: TBD (likely different from US)
- **App Key**: TBD (likely different from US)
- **Base URL**: `https://api.iot.thermomaven.de`

## How It Was Found

### Method: Frida Dynamic Instrumentation

The key was extracted using Frida to hook into the running ThermoMaven Android app and intercept the API calls.

**Steps taken:**
1. Installed ThermoMaven app on a rooted Android device / emulator
2. Used Frida to hook into the app's process
3. Intercepted HTTP requests to capture headers
4. Logged the `x-appId`, `x-sign`, and request parameters
5. Reverse engineered the signature generation by comparing multiple requests
6. Extracted the `app_key` from the signing process

### Key Locations in APK

The key was likely stored in:
- Native libraries (`.so` files) to prevent easy extraction
- Possibly obfuscated in Java/Kotlin code
- Retrieved at runtime through JNI calls

## Signature Algorithm Confirmed

```
MD5(app_key|params_str|body_str)
```

Where:
- `app_key` = `bcd4596f1bb8419a92669c8017bf25e8`
- `params_str` = Sorted headers: `x-appId=...;x-appVersion=...;x-deviceSn=...;x-lang=...;x-nonce=...;x-region=...;x-timestamp=...;x-token=...`
- `body_str` = JSON body without spaces: `{"key":"value"}`

### Important Details

1. **Headers must be sorted alphabetically**
2. **JSON must have no spaces**: Use `json.dumps(data, separators=(',', ':'))`
3. **Password must be MD5 hashed** before sending
4. **Use `data=` not `json=`** when sending the request to preserve exact formatting
5. **Token is `"none"`** (string) before authentication

## Verification

The key was verified by successfully authenticating:

```bash
$ python thermomaven_client.py
Starting ThermoMaven Client...
=== LOGIN ===
AppId: ap4060eff28137181bd
AppKey: bcd4596f1bb8419a92669c8017bf25e8
Status: 200
Response: {
  "code": "0",
  "msg": "Your request has been successful.",
  "data": {
    "token": "...",
    "userId": ...,
    ...
  }
}
✓ Login successful!
🎉 SUCCESS! Logged in!
```

## Tools Used

- **Frida**: Dynamic instrumentation framework
- **Python**: Client implementation
- **Jadx**: APK decompilation (for reference)
- **Android Emulator**: Safe testing environment

## Lessons Learned

1. **Dynamic analysis** (Frida) was more effective than static analysis
2. **Native code** (JNI) is commonly used to hide API keys
3. **Network interception** can reveal the actual values being used
4. **MD5 signatures** are common but not very secure (consider this educational only)

## Next Steps

Now that authentication works, the following can be implemented:

- [x] Login authentication ✅
- [ ] Device listing
- [ ] Device control (temperature, timers, etc.)
- [ ] MQTT connection for real-time updates
- [ ] Historical cooking data
- [ ] Recipe management
- [ ] Home Assistant integration

## Contributing

If you find the EU region keys or additional information:
1. Test the values to verify they work
2. Open an issue or pull request with the details
3. Update this document with the findings

## Ethical Note

This information is provided for:
- **Educational purposes** - Learning about API authentication
- **Personal use** - Controlling your own ThermoMaven devices
- **Home automation** - Integration with Home Assistant

**Please respect ThermoMaven's Terms of Service** and use this responsibly.

## Resources

- Frida documentation: https://frida.re/docs/
- ThermoMaven official site: https://www.thermomaven.com/
- This project: https://github.com/djiesr/ThermoMaven-ha

---

**Status**: ✅ Fully functional for US region authentication  
**Last Updated**: January 2025
